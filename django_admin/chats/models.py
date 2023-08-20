from django.db import models
class AdminRoom(models.Model):
    admin_id = models.CharField(max_length=100)  # Adjust the max length based on your ID format
    admin_username=models.CharField(max_length=100,blank=True,null=True)
    video_room_id=models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AdminRoom: {self.admin_id} ({self.created_at})"