from django.shortcuts import render
from authentication.models import Users
from groups.models import Server

from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserListView(APIView):
    def get(self, request):
        response = Response()
        users = Users.objects.all()  # Retrieve all users from the Users model
        print('users')
        serializer = UserSerializer(users, many=True)  # Serialize the users if needed
        return Response(serializer.data)  # Return the serialized data as the API response

class SendMessage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = request.data.get('content')
        sender_id = request.data.get('sender_id')
        server_id = request.data.get('server_id')

        # Retrieve the authorization token from the request headers
        authorization_header = request.headers.get('Authorization')
        print('authorization_header',authorization_header)
        if authorization_header:
            token = authorization_header.split(' ')[1]
        else:
            return Response({'success': False, 'message': 'Authorization header missing.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            sender = Users.objects.get(id=sender_id)
            server = Server.objects.get(id=server_id)



            return Response({'success': True, 'message': 'Message saved successfully.'}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({'success': False, 'message': 'Sender does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Server.DoesNotExist:
            return Response({'success': False, 'message': 'Server does not exist.'}, status=status.HTTP_404_NOT_FOUND)