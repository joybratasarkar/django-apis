import json
from channels.generic.websocket import AsyncWebsocketConsumer
from groups.models import Message
from authentication.models import Users
from groups.models import Server

from asgiref.sync import sync_to_async


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('self.room_name',self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        print('==========---------------------------------========================')
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
        # print('=-======================================',text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        print('username',username)
        print('self.room_group_name',self.room_name)
        test = await sync_to_async(Server.objects.get)(id=self.room_name)  # Assuming username is unique
        sender = await sync_to_async(Users.objects.get)(user_name=username)  # Assuming username is unique
        # user = Users.objects.get(user_name=username)
        # users = sync_to_async(Users.objects.get(user_name=username))
        print('**************************************************************************')
        print('test',test)
        print('sender',sender)
        # print('receive==================================================================',username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

        # message = Message(content=message, sender=username, Server=self.room_group_name)
        # message = Message.objects.create(content=message, sender=sender, Server=test)
        message = await sync_to_async(Message.objects.create)(content=message, sender=sender, Server=test)
        print('message', message)
        # message = Message(content=message, sender=sender, Server=Server)
        # message.save()

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        print('chatroom_message',message)

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    pass
