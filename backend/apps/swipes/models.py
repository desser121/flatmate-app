import uuid
from django.db import models
from django.conf import settings


class Swipe(models.Model):
    TARGET_CHOICES = [('user', 'Пользователь'), ('listing', 'Объявление')]
    ACTION_CHOICES = [('like', 'Like'), ('dislike', 'Dislike')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='swipes')
    target_type = models.CharField('Тип цели', max_length=10, choices=TARGET_CHOICES)
    target_id = models.UUIDField('ID цели')
    action = models.CharField('Действие', max_length=10, choices=ACTION_CHOICES)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Свайп'
        verbose_name_plural = 'Свайпы'
