from django.contrib.auth import get_user_model
from .models import Match
from apps.chat.models import Conversation

User = get_user_model()


def check_and_create_match(swipe):
    if swipe.action != 'like' or not swipe.is_active:
        return None

    if swipe.target_type == 'user':
        return _check_user_match(swipe)
    elif swipe.target_type == 'listing':
        return _check_listing_match(swipe)
    return None


def _check_user_match(swipe):
    try:
        target_user = User.objects.get(id=swipe.target_id)
    except User.DoesNotExist:
        return None

    reverse_swipe = Swipe.objects.filter(
        author=target_user,
        target_type='user',
        target_id=swipe.author.id,
        action='like',
        is_active=True,
    ).exists()

    if not reverse_swipe:
        return None

    user1_id = min(swipe.author.id.hex, target_user.id.hex)
    user2_id = max(swipe.author.id.hex, target_user.id.hex)

    from uuid import UUID
    user1 = User.objects.get(id=UUID(user1_id))
    user2 = User.objects.get(id=UUID(user2_id))

    match, created = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        listing=None,
    )

    if created:
        Conversation.objects.create(match=match)

    return match if created else None


def _check_listing_match(swipe):
    from apps.listings.models import Listing
    try:
        listing = Listing.objects.get(id=swipe.target_id)
    except Listing.DoesNotExist:
        return None

    if listing.user == swipe.author:
        return None

    reverse_swipe = Swipe.objects.filter(
        author=listing.user,
        target_type='user',
        target_id=swipe.author.id,
        action='like',
        is_active=True,
    ).exists()

    if not reverse_swipe:
        return None

    user1_id = min(swipe.author.id.hex, listing.user.id.hex)
    user2_id = max(swipe.author.id.hex, listing.user.id.hex)

    from uuid import UUID
    user1 = User.objects.get(id=UUID(user1_id))
    user2 = User.objects.get(id=UUID(user2_id))

    match, created = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        listing=listing,
    )

    if created:
        Conversation.objects.create(match=match)

    return match if created else None
