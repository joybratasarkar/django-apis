from django.db import models

# Create your models here.

class Server(models.Model):
    server_name = models.CharField(max_length=100)
    # server_id = models.CharField(max_length=50, unique=True)
    member = models.CharField(max_length=100)
    # no_of_active_users = models.PositiveIntegerField()

    def __str__(self):
        return self.server_name