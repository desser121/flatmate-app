import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import Preference
from apps.listings.models import Listing, ListingPhoto

User = get_user_model()

TEST_USERS = [
    {'phone': '+79001000001', 'password': 'test123', 'name': 'Анна', 'gender': 'female', 'city': 'Москва', 'birth_date': date(2000, 3, 15), 'role_seeker': True, 'role_roommate': True},
    {'phone': '+79001000002', 'password': 'test123', 'name': 'Мария', 'gender': 'female', 'city': 'Москва', 'birth_date': date(1998, 7, 22), 'role_roommate': True},
    {'phone': '+79001000003', 'password': 'test123', 'name': 'Дмитрий', 'gender': 'male', 'city': 'Москва', 'birth_date': date(1995, 11, 8), 'role_seeker': True},
    {'phone': '+79001000004', 'password': 'test123', 'name': 'Елена', 'gender': 'female', 'city': 'Санкт-Петербург', 'birth_date': date(1999, 1, 30), 'role_landlord': True},
    {'phone': '+79001000005', 'password': 'test123', 'name': 'Алексей', 'gender': 'male', 'city': 'Москва', 'birth_date': date(1997, 5, 12), 'role_seeker': True, 'role_roommate': True},
    {'phone': '+79001000006', 'password': 'test123', 'name': 'Ольга', 'gender': 'female', 'city': 'Казань', 'birth_date': date(2001, 9, 5), 'role_seeker': True},
    {'phone': '+79001000007', 'password': 'test123', 'name': 'Сергей', 'gender': 'male', 'city': 'Москва', 'birth_date': date(1993, 12, 18), 'role_landlord': True},
    {'phone': '+79001000008', 'password': 'test123', 'name': 'Наталья', 'gender': 'female', 'city': 'Новосибирск', 'birth_date': date(1996, 4, 25), 'role_roommate': True},
    {'phone': '+79001000009', 'password': 'test123', 'name': 'Иван', 'gender': 'male', 'city': 'Москва', 'birth_date': date(2002, 8, 1), 'role_seeker': True},
    {'phone': '+79001000010', 'password': 'test123', 'name': 'Екатерина', 'gender': 'female', 'city': 'Москва', 'birth_date': date(1994, 6, 14), 'role_seeker': True, 'role_roommate': True},
    {'phone': '+79001000011', 'password': 'test123', 'name': 'Павел', 'gender': 'male', 'city': 'Москва', 'birth_date': date(2000, 2, 28), 'role_seeker': True},
    {'phone': '+79001000012', 'password': 'test123', 'name': 'Татьяна', 'gender': 'female', 'city': 'Екатеринбург', 'birth_date': date(1997, 10, 9), 'role_landlord': True},
]

TEST_PREFERENCES = [
    {'city': 'Москва', 'district': 'Центральный', 'budget_min': 30000, 'budget_max': 60000, 'gender_pref': 'any', 'age_min': 20, 'age_max': 35, 'smoking': 'no', 'pets': 'indifferent', 'schedule': 'any', 'rental_period': 'long'},
    {'city': 'Москва', 'district': 'Северный', 'budget_min': 25000, 'budget_max': 50000, 'gender_pref': 'female', 'age_min': 22, 'age_max': 30, 'smoking': 'no', 'pets': 'no', 'schedule': 'evening', 'rental_period': 'long'},
    {'city': 'Москва', 'district': 'Южный', 'budget_min': 35000, 'budget_max': 70000, 'gender_pref': 'any', 'age_min': 25, 'age_max': 40, 'smoking': 'indifferent', 'pets': 'yes', 'schedule': 'any', 'rental_period': 'any'},
    {'city': 'Санкт-Петербург', 'district': 'Невский', 'budget_min': 20000, 'budget_max': 45000, 'gender_pref': 'any', 'age_min': 18, 'age_max': 35, 'smoking': 'no', 'pets': 'indifferent', 'schedule': 'morning', 'rental_period': 'short'},
    {'city': 'Москва', 'district': 'Западный', 'budget_min': 30000, 'budget_max': 55000, 'gender_pref': 'male', 'age_min': 23, 'age_max': 32, 'smoking': 'no', 'pets': 'no', 'schedule': 'any', 'rental_period': 'long'},
    {'city': 'Казань', 'district': 'Центральный', 'budget_min': 15000, 'budget_max': 30000, 'gender_pref': 'any', 'age_min': 20, 'age_max': 28, 'smoking': 'indifferent', 'pets': 'yes', 'schedule': 'evening', 'rental_period': 'long'},
    {'city': 'Москва', 'district': 'Восточный', 'budget_min': 40000, 'budget_max': 80000, 'gender_pref': 'any', 'age_min': 25, 'age_max': 45, 'smoking': 'no', 'pets': 'indifferent', 'schedule': 'any', 'rental_period': 'any'},
    {'city': 'Новосибирск', 'district': 'Центральный', 'budget_min': 18000, 'budget_max': 35000, 'gender_pref': 'female', 'age_min': 22, 'age_max': 30, 'smoking': 'no', 'pets': 'no', 'schedule': 'morning', 'rental_period': 'long'},
    {'city': 'Москва', 'district': 'Южный', 'budget_min': 25000, 'budget_max': 45000, 'gender_pref': 'any', 'age_min': 20, 'age_max': 28, 'smoking': 'no', 'pets': 'indifferent', 'schedule': 'any', 'rental_period': 'short'},
    {'city': 'Москва', 'district': 'Центральный', 'budget_min': 40000, 'budget_max': 70000, 'gender_pref': 'male', 'age_min': 25, 'age_max': 35, 'smoking': 'no', 'pets': 'yes', 'schedule': 'evening', 'rental_period': 'long'},
    {'city': 'Москва', 'district': 'Северный', 'budget_min': 20000, 'budget_max': 40000, 'gender_pref': 'any', 'age_min': 20, 'age_max': 30, 'smoking': 'indifferent', 'pets': 'no', 'schedule': 'any', 'rental_period': 'short'},
    {'city': 'Екатеринбург', 'district': 'Кировский', 'budget_min': 15000, 'budget_max': 35000, 'gender_pref': 'any', 'age_min': 22, 'age_max': 40, 'smoking': 'no', 'pets': 'indifferent', 'schedule': 'any', 'rental_period': 'long'},
]

TEST_LISTINGS = [
    {'user_idx': 3, 'listing_type': 'rent', 'property_type': 'room', 'city': 'Санкт-Петербург', 'district': 'Невский', 'budget_min': 20000, 'budget_max': 25000, 'description': 'Комната в уютной 3-комнатной квартире рядом с метро. Есть все удобства.'},
    {'user_idx': 6, 'listing_type': 'rent', 'property_type': 'apartment', 'city': 'Москва', 'district': 'Восточный', 'budget_min': 50000, 'budget_max': 65000, 'description': 'Студия в новостройке. Ремонт, мебель, техника. До метро 5 минут.'},
    {'user_idx': 11, 'listing_type': 'rent', 'property_type': 'room', 'city': 'Екатеринбург', 'district': 'Кировский', 'budget_min': 18000, 'budget_max': 22000, 'description': 'Комната в двухкомнатной квартире. Тихий район, рядом парк.'},
]


class Command(BaseCommand):
    help = 'Создаёт тестовые данные'

    def handle(self, *args, **options):
        self.stdout.write('Создаю тестовых пользователей...')

        users = []
        for i, data in enumerate(TEST_USERS):
            user, created = User.objects.get_or_create(
                phone=data['phone'],
                defaults={
                    'name': data['name'],
                    'gender': data['gender'],
                    'city': data['city'],
                    'birth_date': data['birth_date'],
                    'role_seeker': data.get('role_seeker', False),
                    'role_roommate': data.get('role_roommate', False),
                    'role_landlord': data.get('role_landlord', False),
                }
            )
            if created:
                user.set_password(data['password'])
                user.save()
            users.append(user)
            self.stdout.write(f'  {"+" if created else "~"} {user.name} ({user.phone})')

        self.stdout.write('\nСоздаю предпочтения...')
        for i, user in enumerate(users):
            if i < len(TEST_PREFERENCES):
                pref_data = TEST_PREFERENCES[i]
                pref, created = Preference.objects.get_or_create(
                    user=user,
                    defaults=pref_data
                )
                self.stdout.write(f'  {"+" if created else "~"} {user.name}')

        self.stdout.write('\nСоздаю тестовые объявления...')
        for data in TEST_LISTINGS:
            user = users[data['user_idx']]
            listing, created = Listing.objects.get_or_create(
                user=user,
                city=data['city'],
                defaults={
                    'listing_type': data['listing_type'],
                    'property_type': data['property_type'],
                    'district': data.get('district', ''),
                    'budget_min': data['budget_min'],
                    'budget_max': data['budget_max'],
                    'description': data['description'],
                }
            )
            self.stdout.write(f'  {"+" if created else "~"} {listing}')

        self.stdout.write(self.style.SUCCESS('\nГотово! Создано 12 тестовых пользователей.'))
        self.stdout.write('Для входа используй любой номер телефона + пароль test123')
