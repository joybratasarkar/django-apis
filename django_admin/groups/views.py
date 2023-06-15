from django.shortcuts import render
from authentication.models import Users
from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from .models import Server,ServerUsers,Message
from .serializers import ServerSerializer,MessageSerializer
import random
import string
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ServerName(APIView):
    def post(self, request):
        user_id = request.data['user_name']
        server_name = request.data['server_name']
        id = request.data['id']
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response(f"User with id '{id}' does not exist", status=400)

        server = Server.objects.create(server_name=server_name,_id=id)
        server.user.add(user)

        return Response({
            'id': id,
            'server_name': server.server_name,
            'user_name': user.user_name,
        }, status=201)



class AddServerName(APIView):
    def post(self, request):
        user_id = request.data['user_name']
        server_name = request.data['server_name']
        id = request.data['id']
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response(f"User with id '{id}' does not exist", status=400)
        server = Server.objects.create(server_name=server_name, _id=id)
        server_user.id = _id
        server_user.save()
        # server.server.add(user)

        return Response({
            'id': id,   
            'server_name': server.server_name,
            'user_name': user.user_name,
        }, status=201)



class GetServerName(APIView):
    def get(self, request):
        params = request.query_params.get('params')  # Get the value of the 'user_id' parameter from the URL
        print('params---------------------------------',params)
        user = request.user  # Get the authenticated user
        # servers = Server.objects.filter(_id=params)  # Retrieve servers belonging to the user
        servers = Server.objects.all()
        # print('servers',servers)
        data = []
        for server in servers:
            # print('server',server)
            server_data = { 
                'id': server.id,
                '_id': server._id,
                'server_name': server.server_name,
                # 'users': []
            }
            data.append(server_data)
        
        return Response(data)



       
class GetAllServerName(APIView):
    def get(self, request):
        
        servers = Server.objects.all()  # Retrieve all server instances
        data = []
        for server in servers:
            server_data = { 
                'id': server._id,
                'server_name': server.server_name,
            }
            data.append(server_data)
        
        return Response(data)

class GetMessage(APIView):
    def get(self, request):
        params = request.query_params.get('params')
        print('params',params)
        # Use a case-insensitive filter query to retrieve matching messages
        param_value = str(params)
        matching_messages = Message.objects.filter(Server__id__iexact=param_value).order_by('-timestamp')
        print('matching_messages',matching_messages)
        serializer = MessageSerializer(matching_messages, many=True)

        if matching_messages:
            return Response(serializer.data, status=201)
        else:
            return Response(status=204)

