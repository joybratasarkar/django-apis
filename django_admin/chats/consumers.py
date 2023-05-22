import json
from channels.generic.websocket import AsyncWebsocketConsumer
from groups.models import Message


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('self',self)
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
        print('receive',message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )
        # message = Message(content=message, sender=username, Server=self.room_group_name)
        # print('message',message)
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
