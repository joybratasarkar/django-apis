import json
from channels.generic.websocket import AsyncWebsocketConsumer
from groups.models import Message
from authentication.models import Users
from groups.models import Server
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import threading
from .tasks import create_message
from channels.generic.websocket import WebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # print('self.room_name',self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        server = await database_sync_to_async(Server.objects.get)(id=self.room_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # print('disconnect',self)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        # time = text_data_json['time']
        chat_room_id = int(text_data_json['chat_room_id'])
        print('chat_room_id---------------------------------------------',chat_room_id)
        # Get the Users and Server objects asynchronously using database_sync_to_async
        users = await database_sync_to_async(Users.objects.get)(user_name=username)
        server = await database_sync_to_async(Server.objects.get)(id=self.room_name)

        # Create the Message object
        # message_task = create_message.delay(message, username, self.room_name)
        # message_result = await get_message_result(message_task)

        # # Create the Message object
        message_obj = await database_sync_to_async(Message.objects.create)(
            content=message,
            sender=users,
            Server=server
        )
        # message = await database_sync_to_async(Message.objects.create)(content=message, sender=users, Server=server )
        # message_obj = await database_sync_to_async(Message.objects.create)(
        #     content=message,
        #     sender=users,
        #     Server=server
        # )


        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
                # 'Messagetype':'sender'
            }
        )
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        # print('message',message)
        # print('username',username)
        # print('chatroom_message================test',message)
        users = await database_sync_to_async(Users.objects.get)(user_name=username)
        server = await database_sync_to_async(Server.objects.get)(id=self.room_name)

        # Create the Message object
        # message = Message.objects.create(content=message, sender=users, Server=server)
        
        # message = await database_sync_to_async(Message.objects.create)(content=message, sender=users, Server=server,Messagetype='sender')
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
async def get_message_result(message_task):
    return await sync_to_async(message_task.get)()
    pass




class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'webrtc_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     message = json.loads(text_data)
    #     print('--------------------------',message)
    #     event = message['event']
    #     # print('event',event)
    #     # data = message['data']

    #     # Handle different event types
    #     if event == 'create' or event == 'offer' or event == 'answer' or event == 'candidate' or event == 'hangUp':
    #         # Broadcast the message to the room group
    #         await self.channel_layer.group_send(
    #             self.room_group_name,
    #             {
    #                 'type': 'handle_message',
    #                 'event': event,
    #                 # 'datmessagea': data
    #             }
    #         )

    # async def receive(self, text_data):
    #     message = json.loads(text_data)
    #     event = message['type']
    #     # Handle different event types
    #     if event == 'create' or event == 'offer' or event == 'candidate' or event == 'hangUp':
    #         # Broadcast the message to the room group
    #         await self.channel_layer.group_send(
    #             self.room_group_name,
    #             {
    #                 'type': 'handle_message',
    #                 'event': event,
    #                 'data': message.get('data')  # Use get() method to retrieve the value safely
    #             }
    #         )
    #     elif event == 'answer':
    #         # Broadcast the answer message to a specific recipient
    #         recipient = message.get('recipient')
    #         if recipient:
    #             await self.channel_layer.send(
    #                 recipient,
    #                 {
    #                     'type': 'handle_message',
    #                     'event': event,
    #                     'data': message.get('data')
    #                 }
    #             )
    async def receive(self, text_data):
        message = json.loads(text_data)
        event = message['type']
        id = message['id']
        chat_room_id=message['chat_room_id']
        print(event)
        # Handle different event types
        # if event == 'create' or event == 'offer' or event == 'answer' or event == 'candidate' or event == 'hangUp':
            # Broadcast the message to the room group
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'handle_message',
                    'event': event,
                    'data': message.get('data')  # Use get() method to retrieve the value safely
                }
            )
    # Receive message from room group
    async def handle_message(self, event):
        # Send message to WebSocket
        # print(event['event'])
                # if event == 'create' or event == 'offer' or event == 'answer' or event == 'candidate' or event == 'hangUp':

        await self.send(text_data=json.dumps({
            'event': event['event'],
            'data': event['data'],
            # 'id':event['id']
        }))
