from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    confirmation_code = models.CharField(max_length=4, blank=True)

    # Добавляем уникальные related_name, чтобы избежать конфликта
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Уникальный related_name для группы
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Уникальный related_name для разрешений
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
