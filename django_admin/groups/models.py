from django.db import models
from random import randint
from authentication.models import Users
from datetime import datetime

# Create your models here.

class Server(models.Model):
    server_name = models.CharField(max_length=100)
    # server_id = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, editable=False)
    # member = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(100000, 1000000)
                is_id_exist = Server.objects.filter(id=id).exists()
                
            self.id = id

        super().save(*args, **kwargs)


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    Server = models.ForeignKey(Server, on_delete=models.CASCADE)

    def __str__(self):
        return self.content