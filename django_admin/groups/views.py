from django.shortcuts import render
from authentication.models import Users
from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from .models import Server,ServerUsers,Message
from .serializers import ServerSerializer,MessageSerializer
import random
import string
from rest_framework.response import Response
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

        # server = Server.objects.create(server_name=server_name,_id=id)
        # server.user.add(user)
        # server_user = ServerUsers.objects.create(server=server_name, user=user, id=id)
        # server_user = ServerUsers.objects.create(server=server, user=user)
        server = Server.objects.create(server_name=server_name, _id=id)
        # server_user = ServerUsers.objects.create(server=server, user=user, _id=id)
        # Set the 'id' field of the ServerUsers instance
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
        
        user = request.user  # Get the authenticated user
        # servers = Server.objects.filter(_id=params)  # Retrieve servers belonging to the user
        servers = Server.objects.all()
        data = []
        for server in servers:
            server_data = { 
                'id': server.id,
                '_id': server._id,
                'server_name': server.server_name,
                'users': []
            }
            for user in server.user.all():
                print('user',user)
                user_data = {
                    'id': user.id,
                    'user_name': user.user_name,
                    # Include any other user fields you want in the response
                }
                server_data['users'].append(user_data)
            
            data.append(server_data)
        
        return Response(data)

# class GetServerName(APIView):
#     def get(self, request):
#         user_id = request.query_params.get('params')  # Get the value of the 'user_id' parameter from the URL

#         try:
#             user = Users.objects.get(user_name=user_id)  # Retrieve the user based on the user_id
#         except Users.DoesNotExist:
#             return Response(f"User with id '{user_id}' does not exist", status=400)
#         print('---------------',user)
#         servers = Server.objects.filter(members=user)  # Retrieve servers where the user is a member
#         print('servers','-----------------------------',servers)
#         data = []
#         for server in servers:
#             server_data = { 
#                 'id': server.id,
#                 'server_name': server.server_name,
#             }
#             data.append(server_data)
#         return Response(data)  # Return the modified data as the API response

       
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


# class GetMessage(APIView):
#     def get(self, request):
#         params = request.query_params.get('params')
#         print('params',params)
#         messages = Message.objects.all()
#         serializer = MessageSerializer(messages, many=True)

#             # print('serializer',serializer)
#         # return Response({
#         #  serializer.data,
#         # }, status=201)
#         return Response(serializer.data)
# class GetMessage(APIView):
#     def get(self, request):
#         params = request.query_params.get('params')
#         print('paramstest34', params)
#         messages = Message.objects.all()
#         serializer = MessageSerializer(messages, many=True)
#         for server in serializer.data:  # Assuming `Server` is an array of dictionaries
#             print(server['Server'])
#             print(server['Server'] == params)
#             if server['Server'] == params:  # Replace `field_name` with the actual field name to compare
#                 print('inside')
#                 return Response(serializer.data, status=201)
        
#         return Response(status=204)  # No content response
class GetMessage(APIView):
    def get(self, request):
        params = request.query_params.get('params')
        print('paramstest34', params)
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        matching_servers = []
        for server in serializer.data:
            server_value = str(server['Server'])  # Convert to string
            param_value = str(params)  # Convert to string
            if server_value.strip().lower() == param_value.strip().lower():
                matching_servers.append(server)
        
        if matching_servers:
            return Response(matching_servers, status=201)
        else:
            return Response(status=204)

