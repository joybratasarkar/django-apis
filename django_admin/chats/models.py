from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    google_id = models.CharField(max_length=255, default='')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='chats_user_set',  # Change related_name for groups
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='chats_user_set',  # Change related_name for user_permissions
        related_query_name='user'
    )
