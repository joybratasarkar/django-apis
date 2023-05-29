import json
from channels.generic.websocket import AsyncWebsocketConsumer
from groups.models import Message
from authentication.models import Users
from groups.models import Server
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print('self.room_name',self.room_name)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('self.room_name',self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        server = await database_sync_to_async(Server.objects.get)(id=self.room_name)

        print('server===============================',server)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect',self)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Get the Users and Server objects asynchronously using database_sync_to_async
        users = await database_sync_to_async(Users.objects.get)(user_name=username)
        server = await database_sync_to_async(Server.objects.get)(id=self.room_name)

        # Create the Message object
        # message = Message.objects.create(content=message, sender=users, Server=server)
        # Messagetype='sender'
        message = await database_sync_to_async(Message.objects.create)(content=message, sender=users, Server=server )

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message.content,
                'username': username,
                # 'Messagetype':'sender'
            }
        )
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        print('message',message)
        print('username',username)
        print('chatroom_message================test',message)
        users = await database_sync_to_async(Users.objects.get)(user_name=username)
        server = await database_sync_to_async(Server.objects.get)(id=self.room_name)

        # Create the Message object
        # message = Message.objects.create(content=message, sender=users, Server=server)
        
        # message = await database_sync_to_async(Message.objects.create)(content=message, sender=users, Server=server,Messagetype='sender')
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    pass
