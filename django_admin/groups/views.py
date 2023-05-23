from django.shortcuts import render
from authentication.models import Users
from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from .models import Server
from .serializers import ServerSerializer
import random
import string
from rest_framework.response import Response

# Create your views here.
# class UserListView(APIView):
#     def get(self, request):

#         response = Response()
#         users = Users.objects.all()  # Retrieve all users from the Users model
#         print('users')
#         serializer = UserSerializer(users, many=True)  # Serialize the users if needed
#         return Response(serializer.data)  # Return the serialized data as the API response


class ServerName(APIView):
    def post(self, request):
        user_name = request.data['user_name']
        server_name = request.data['server_name']
        print('user_name============', request.data)

        try:
            user = Users.objects.get(user_name=user_name)
        except Users.DoesNotExist:
            return Response(f"User with username '{user_name}' does not exist", status=400)

        server = Server.objects.create(user_name=user, server_name=server_name)

        return Response({
            'id': server.id,
            'server_name': server.server_name,
            'user_name': server.user_name.user_name,
        }, status=201)

class GetServerName(APIView):
    def get(self, request):
        print('=-===============')
        params = request.query_params.get('params')  # Get the value of the 'user_id' parameter from the URL

        user = request.user  # Get the authenticated user
        servers = Server.objects.filter(user_name=params)  # Retrieve servers belonging to the user

        # servers = Server.objects.all();
        print('servers----------------------',servers)
        data = []
        for server in servers:
            print('servers=--------','==========',server,'------------------', server.id, '-----', server.server_name, '-----', server.user_name)
            server_data = { 
                'id': server.id,
                'server_name': server.server_name,
            }
            data.append(server_data)
        return Response(data)  # Return the modified data as the API response


       
