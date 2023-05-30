from celery import shared_task
from channels.db import database_sync_to_async
from groups.models import Message
from authentication.models import Users
from groups.models import Server

@shared_task
def create_message(content, username, room_name):
    # Get the Users and Server objects asynchronously using database_sync_to_async
    print('------------------------inSide Tasks',content,room_name,username)
    users = Users.objects.get(user_name=username)
    server = Server.objects.get(id=room_name)

    # Create the Message object
    message = Message.objects.create(content=content, sender=users, Server=server)
    print('insideaasdasd=-0--00000000000000000000000000000000',message)
    return message.content
