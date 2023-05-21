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
        # server_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        # print('server_id',server_id)
        # request.data['server_id'] = server_id
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class GetServerName(APIView):
    def get(self, request):

        response = Response()
        users = Server.objects.all()  # Retrieve all users from the Users model
        print('users')
        serializer = ServerSerializer(users, many=True)  # Serialize the users if needed
        return Response(serializer.data)  # Return the serialized data as the API response
       
       
        #     def post(self, request):
        # server_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        # print('server_id',server_id)
        # print('Server.objects.filter(server_id=server_id).exists()',Server.objects.filter(server_id=server_id).exists())
        # while Server.objects.filter(server_id=server_id).exists():
        #     server_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        # request.data['server_id'] = server_id
        # serializer = ServerSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data, status=201)
        # return Response(serializer.errors, status=400)