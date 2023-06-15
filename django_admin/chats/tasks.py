from celery import shared_task
from channels.db import database_sync_to_async
from groups.models import Message
from authentication.models import Users
from groups.models import Server
import logging
logger = logging.getLogger(__name__)
logging.getLogger('').setLevel(logging.DEBUG)

@shared_task
def create_message(content, username, room_name):
    try:
        print('Z################################')
        logger.debug("Creating message: content={}, username={}, room_name={}".format(content, username, room_name))
    # Get the Users and Server objects asynchronously using database_sync_to_async
        users = Users.objects.get(user_name=username)
        server = Server.objects.get(id=room_name)

        # Create the Message object
        # message = Message.objects.create(content=content, sender=users, Server=server)
        message =Message.objects.create(
            content=message_result,
            sender=users,
            Server=server
        )
        return message.content

    except Exception as e:
        logger.exception("An error occurred while creating the message")
        raise e
