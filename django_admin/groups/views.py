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
class UserListView(APIView):
    def get(self, request):

        response = Response()
        users = Users.objects.all()  # Retrieve all users from the Users model
        print('users')
        serializer = UserSerializer(users, many=True)  # Serialize the users if needed
        return Response(serializer.data)  # Return the serialized data as the API response


class ServerName(APIView):
    def post(self, request):
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            server = serializer.save()  # Save the serializer object and get the saved Server instance
            return Response({
                'id': server.id,
                'server_name': server.server_name,
            }, status=201)
        return Response(serializer.errors, status=400)

class GetServerName(APIView):
    def get(self, request):
        print('request',request)
        servers = Server.objects.all()  # Retrieve all Server instances
        # token = request.COOKIES.get('jwt')
        # token = request.COOKIES.get('jwt') or request.session.get('jwt')

        # Create a list to store the serialized data with the required fields
        data = []
        for server in servers:
            server_data = {
                'id': server.id,
                'server_name': server.server_name,
            }
            data.append(server_data)

        return Response(data)  # Return the serialized data as the API response
       
