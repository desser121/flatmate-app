from django.contrib.auth import get_user_model
from apps.swipes.models import Swipe

User = get_user_model()


def calculate_user_compatibility(user, candidate):
    score = 0.0

    pref = getattr(user, 'preference', None)
    cand_pref = getattr(candidate, 'preference', None)

    if not pref:
        return 50.0

    if pref.city and candidate.city:
        score += 25.0 if pref.city.lower() == candidate.city.lower() else 0.0

    if pref.district and cand_pref and cand_pref.district:
        if pref.district.lower() == cand_pref.district.lower():
            score += 15.0
        else:
            score += 3.0

    if (pref.budget_min or pref.budget_max) and (cand_pref and (cand_pref.budget_min or cand_pref.budget_max)):
        bmin1, bmax1 = pref.budget_min or 0, pref.budget_max or 999999
        bmin2, bmax2 = cand_pref.budget_min or 0, cand_pref.budget_max or 999999
        overlap = min(bmax1, bmax2) - max(bmin1, bmin2)
        total = max(bmax1, bmax2) - min(bmin1, bmin2)
        if total > 0:
            score += 20.0 * max(0, overlap / total)

    if pref.gender_pref != 'any':
        score += 10.0 if candidate.gender == pref.gender_pref else 0.0
    else:
        score += 10.0

    if candidate.age and pref.age_min and pref.age_max:
        if pref.age_min <= candidate.age <= pref.age_max:
            score += 10.0
        else:
            diff = min(abs(candidate.age - pref.age_min), abs(candidate.age - pref.age_max))
            score += max(0, 10.0 - diff)

    if cand_pref:
        if pref.smoking == 'indifferent' or cand_pref.smoking == 'indifferent':
            score += 10.0
        elif pref.smoking == cand_pref.smoking:
            score += 10.0

        if pref.pets == 'indifferent' or cand_pref.pets == 'indifferent':
            score += 10.0
        elif pref.pets == cand_pref.pets:
            score += 10.0

    return round(score, 1)


def calculate_listing_compatibility(user, listing):
    score = 0.0
    pref = getattr(user, 'preference', None)

    if not pref:
        return 50.0

    if pref.city and listing.city:
        score += 25.0 if pref.city.lower() == listing.city.lower() else 0.0

    if pref.district and listing.district:
        if pref.district.lower() == listing.district.lower():
            score += 20.0
        else:
            score += 5.0

    if pref.budget_min or pref.budget_max:
        bmin, bmax = pref.budget_min or 0, pref.budget_max or 999999
        if bmin <= listing.budget_min <= bmax:
            score += 30.0
        elif listing.budget_max <= bmax:
            score += 20.0

    score += 15.0

    score += 10.0

    return round(score, 1)


def get_swiped_target_ids(user, target_type):
    swipes = Swipe.objects.filter(
        author=user,
        target_type=target_type,
        is_active=True,
    ).values_list('target_id', flat=True)
    return set(str(s) for s in swipes)


def get_feed(user, target_type='user'):
    if target_type == 'user':
        return _get_user_feed(user)
    else:
        return _get_listing_feed(user)


def _get_user_feed(user):
    swiped_ids = get_swiped_target_ids(user, 'user')

    candidates = User.objects.filter(is_active=True).exclude(id=user.id)

    pref = getattr(user, 'preference', None)
    if pref and pref.city:
        candidates = candidates.filter(city__iexact=pref.city)

    items = []
    for candidate in candidates:
        if str(candidate.id) in swiped_ids:
            continue

        score = calculate_user_compatibility(user, candidate)

        primary_photo = candidate.photos.filter(is_primary=True).first()
        if not primary_photo:
            primary_photo = candidate.photos.first()

        photo_url = primary_photo.image.url if primary_photo else ''

        items.append({
            'type': 'user',
            'id': str(candidate.id),
            'name': candidate.name,
            'age': candidate.age,
            'gender': candidate.get_gender_display() if candidate.gender else '',
            'city': candidate.city,
            'bio': candidate.bio,
            'photo': photo_url,
            'compatibility': score,
        })

    items.sort(key=lambda x: x['compatibility'], reverse=True)
    return items


def _get_listing_feed(user):
    from apps.listings.models import Listing

    swiped_ids = get_swiped_target_ids(user, 'listing')

    pref = getattr(user, 'preference', None)
    listings = Listing.objects.filter(is_active=True).exclude(user=user)

    if pref and pref.city:
        listings = listings.filter(city__iexact=pref.city)

    listings = listings.exclude(id__in=swiped_ids if swiped_ids else [])

    items = []
    for listing in listings:
        score = calculate_listing_compatibility(user, listing)

        primary_photo = listing.photos.first()
        photo_url = primary_photo.image.url if primary_photo else ''

        items.append({
            'type': 'listing',
            'id': str(listing.id),
            'name': listing.get_property_type_display(),
            'city': listing.city,
            'district': listing.district,
            'address': listing.address,
            'photo': photo_url,
            'compatibility': score,
            'listing_type': listing.get_listing_type_display(),
            'property_type': listing.get_property_type_display(),
            'budget_min': listing.budget_min,
            'budget_max': listing.budget_max,
            'description': listing.description,
        })

    items.sort(key=lambda x: x['compatibility'], reverse=True)
    return items
