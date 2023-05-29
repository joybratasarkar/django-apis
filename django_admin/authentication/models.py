
# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime
import uuid
from random import randint

class Users(AbstractUser):
    user_name = models.CharField(max_length=255,unique=True,primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    google_id = models.CharField(max_length=255, default='')
    # uuid=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    id = models.IntegerField(editable=False,default=0)
    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(100000, 1000000)
                is_id_exist = Users.objects.filter(id=id).exists()
                
            self.id = id

        super().save(*args, **kwargs)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='auth',  # Change related_name for groups
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='chats_user_set',  # Change related_name for user_permissions
        related_query_name='user'
    )


class BaseModel(models.Model):
    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(null=True,blank=True)
    is_deleted=models.DateTimeField(default=False)
    uuid=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    
    def soft_delete(self):
        self.deleted_at=datetime.utcnow()
        self.is_deleted=True
        self.save()
