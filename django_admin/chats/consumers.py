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
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from chats.models import AdminRoom
from django.core.cache import cache
import jwt
from rest_framework.response import Response

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
                # Broadcast the new join event to all participants



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
        # recipient_socket_id = text_data['recipient_socket_id']  # Assume this is provided in the signaling message

        # print('chat_room_id---------------------------------------------',chat_room_id)
        # print('-----------------self.room_name',self.room_name)
        # print('=================message',message)
        # Get the Users and Server objects asynchronously using database_sync_to_async
        users = await database_sync_to_async(Users.objects.get)(user_name=username)
        server = await database_sync_to_async(Server.objects.get)(id=chat_room_id)

        # print('debugger;',users)
        # print('server',server)
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

            # self.room_group_name,

        # Send the message to the group
        await self.channel_layer.group_send(
            username,
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
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'webrtc_%s' % self.room_name
        # self.connected_peers = set()
        print('self.connected_peers',self.id)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(self.id)
        # # await self.join_room()
        isAdmin = await database_sync_to_async(AdminRoom.objects.filter(admin_id=self.id).exists)()
        print('isAdmin',isAdmin)
        if isAdmin:
            # The peer with 'admin' ID creates the room
            await self.create_room()
        else:
            # Other peers join the existing room
            await self.join_room()



    async def join_room(self):
        # Handle joining the existing room
        username = self.id
        message = f'{username} joined the room {self.room_name}'
        print('-----------------------new joiner--------', message)
        
        # Send the message to the WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_Join',
                # 'event': 'new_join',
                'data': {
                    'message': message
                }
            }
        )
    async def new_Join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_join',
            'data': event['data'],
            'event': event,
        }))

    async def send_offer_to_peer(self, peer_id, offer_data):
        if peer_id not in self.connected_peers:
            await self.channel_layer.send(
                self.room_group_name,
                {
                    'type': 'handle_message',
                    'event': 'send_offer',
                    'data': {
                        'peer_id': peer_id,
                        'offer_data': offer_data
                    }
                }
            )
            self.connected_peers.add(peer_id)
    async def receive(self, text_data):
        message = json.loads(text_data)
        print('message',message)
        event = message['type']
        eventType = message['type']
        id=message['id']
        user_name = message['user_name']
        video_roomID = int(message['video_roomID'])
        signalingState = message['signalingState']

        if eventType == 'offer':
            print('----------------------offer-----------', self.room_name)
            name = message['user_name']
            # print('self.channel_name',self.channel_name)
            offer_message = {
                'type': 'call_received',
                'data': {
                    'caller': name,
                    'rtcMessage': message['data']['sdp']
                }
            }   
            # Send the offer message to the group, excluding the sender
            await self.send_offer_to_peer(id, message['data']['sdp'])

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': name,
                        'rtcMessage': message['data']['sdp']
                    },
                    'message': offer_message,
                    # 'exclude': exclude_sender_channel
                }
            )
        if eventType == 'answer':
            name = message['user_name']
            # print('----------------------offer-----------', self.room_name)

            await self.channel_layer.group_send(
                 self.room_group_name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': name,
                        'rtcMessage': message['data']['sdp']
                    },
                'exclude': self.channel_name  # Exclude the sender's channel
                }
            )
        if eventType == 'ice-candidate':
            name = message['user_name']
            # print('----------------------ICEcandidate-----------', self.room_name)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'caller': name,
                        # 'rtcMessage': message['data']['sdp']
                    }
                }
            )

        if eventType == 'admin':
            # Check if an AdminRoom entry with the given admin_id (user_name) already exists
            isAdminSaved = await database_sync_to_async(AdminRoom.objects.filter(admin_id=id).exists)()
            if not isAdminSaved:
                # If an entry doesn't exist, create a new AdminRoom entry
                admin = await database_sync_to_async(AdminRoom.objects.create)(
                    admin_id=id,
                    admin_username=user_name,
                    video_room_id=video_roomID
                )
                await self.create_room()

            # Create the room (assuming this is a method within the same class)
            





    async def create_room(self):
        # Handle the room creation by the admin
        # print('self')
        message = f'Room {self.room_name} id created by  Admin id {self.id}'
        print('-----------------------Admin joined the --------', message)
        await self.send(text_data=json.dumps({
            'type': 'admin_Create_Room',
            'message': message
        }))
  


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


    async def call_received(self, event):
        print('-----------------------------------------------call_received------------------------------')
        # print(event['data'])
        # print('Call received by ', self.my_name )
        await self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data'],
            'event': event,
        }))

    async def call_answered(self, event):

        # print(event)
        await print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data'],
            'event': event,

        }))

    async def ICEcandidate(self, event):
        # print('=============================ICEcandidate==================================================')
        await self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data'],
            'event': event,
        }))































