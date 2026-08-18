import uuid
from django.db import models
from django.conf import settings


class Listing(models.Model):
    TYPE_CHOICES = [
        ('rent', 'Сдаю'),
        ('seek', 'Ищу жильё'),
        ('seek_roommate', 'Ищу соседа'),
    ]
    PROPERTY_CHOICES = [
        ('room', 'Комната'),
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('bed', 'Койко-место'),
        ('shared', 'Совместная аренда'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    listing_type = models.CharField('Тип объявления', max_length=20, choices=TYPE_CHOICES)
    property_type = models.CharField('Тип жилья', max_length=20, choices=PROPERTY_CHOICES)
    city = models.CharField('Город', max_length=100)
    district = models.CharField('Район', max_length=100, blank=True, default='')
    address = models.CharField('Адрес', max_length=500, blank=True, default='')
    latitude = models.DecimalField('Широта', max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=11, decimal_places=8, null=True, blank=True)
    budget_min = models.PositiveIntegerField('Мин. бюджет', default=0)
    budget_max = models.PositiveIntegerField('Макс. бюджет', default=0)
    description = models.TextField('Описание', blank=True, default='')
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'{self.get_listing_type_display()} - {self.get_property_type_display()} ({self.city})'


class ListingPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField('Фото', upload_to='listings/photos/')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
