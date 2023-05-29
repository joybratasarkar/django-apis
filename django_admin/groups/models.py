from django.db import models
from random import randint
from authentication.models import Users
from datetime import datetime

# Create your models here.



class Server(models.Model):
    server_name = models.CharField(max_length=100)
    user = models.ManyToManyField('ServerUsers', related_name='servers', blank=True)
    # user = models.ManyToManyField(Users, related_name='servers', blank=True)
    # user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE, db_column='user_id', related_name='created_servers')
    _id = models.CharField(editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True,unique=True)

    def save(self, *args, **kwargs):
        if not self.id and not self._id:
            is_id_exist = True
            while is_id_exist:
                id = randint(100000, 1000000)
                is_id_exist = Server.objects.filter(_id=id).exists()
            self._id = id
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

class ServerUsers(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='server_users',blank=True,null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_servers',blank=True,null=True)
    _id = models.IntegerField(default=0,null=True,editable=True,db_index=True,unique=False)  # Provide a default value for id field
    # _id = models.CharField(null=True,editable=True,db_index=True,unique=False)  # Provide a default value for id field
    # _id = models.BigIntegerField(null=True, editable=True, unique=False)
    # _id = models.IntegerField(null=True, editable=True, unique=False)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    Server = models.ForeignKey(Server, on_delete=models.CASCADE,null=True)
    Messagetype=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.content