import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField('Телефон', max_length=20, unique=True)
    name = models.CharField('Имя', max_length=100, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=10, choices=GENDER_CHOICES, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    bio = models.TextField('О себе', blank=True, default='')
    role_seeker = models.BooleanField('Ищу жильё', default=False)
    role_roommate = models.BooleanField('Ищу соседа', default=False)
    role_landlord = models.BooleanField('Сдаю жильё', default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} ({self.phone})'

    @property
    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    @property
    def profile_complete(self):
        return all([
            self.name,
            self.birth_date,
            self.city,
            self.gender,
            (self.role_seeker or self.role_roommate or self.role_landlord),
            self.photos.exists(),
        ])


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField('Фото', upload_to='users/photos/')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_primary = models.BooleanField('Главное фото', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото пользователя'
        verbose_name_plural = 'Фото пользователей'


class Preference(models.Model):
    SMOKING_CHOICES = [('yes', 'Да'), ('no', 'Нет'), ('indifferent', 'Не важно')]
    PETS_CHOICES = [('yes', 'Да'), ('no', 'Нет'), ('indifferent', 'Не важно')]
    SCHEDULE_CHOICES = [('morning', 'Утренний'), ('evening', 'Вечерний'), ('any', 'Любой')]
    RENTAL_CHOICES = [('short', 'Краткосрочно'), ('long', 'Долгосрочно'), ('any', 'Любой')]
    GENDER_PREF_CHOICES = [('male', 'Мужской'), ('female', 'Женский'), ('any', 'Любой')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    city = models.CharField('Город', max_length=100, blank=True, default='')
    district = models.CharField('Район', max_length=100, blank=True, default='')
    budget_min = models.PositiveIntegerField('Мин. бюджет', default=0)
    budget_max = models.PositiveIntegerField('Макс. бюджет', default=0)
    gender_pref = models.CharField('Предпочтение по полу', max_length=10, choices=GENDER_PREF_CHOICES, default='any')
    age_min = models.PositiveIntegerField('Мин. возраст', default=18)
    age_max = models.PositiveIntegerField('Макс. возраст', default=100)
    smoking = models.CharField('Курение', max_length=15, choices=SMOKING_CHOICES, default='indifferent')
    pets = models.CharField('Животные', max_length=15, choices=PETS_CHOICES, default='indifferent')
    schedule = models.CharField('График', max_length=15, choices=SCHEDULE_CHOICES, default='any')
    rental_period = models.CharField('Срок аренды', max_length=15, choices=RENTAL_CHOICES, default='any')

    class Meta:
        verbose_name = 'Предпочтения'
        verbose_name_plural = 'Предпочтения'
