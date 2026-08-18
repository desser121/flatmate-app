import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('match', 'Матч'),
        ('message', 'Сообщение'),
        ('viewing', 'Просмотр'),
        ('system', 'Система'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)
    title = models.CharField('Заголовок', max_length=200)
    body = models.TextField('Текст', blank=True, default='')
    reference_type = models.CharField('Тип объекта', max_length=50, blank=True, default='')
    reference_id = models.UUIDField('ID объекта', null=True, blank=True)
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
