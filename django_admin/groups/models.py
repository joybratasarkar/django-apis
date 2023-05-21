from django.db import models
from random import randint

# Create your models here.

class Server(models.Model):
    server_name = models.CharField(max_length=100)
    # server_id = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, editable=False)
    member = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(100000, 1000000)
                is_id_exist = Server.objects.filter(id=id).exists()
                
            self.id = id

        super().save(*args, **kwargs)