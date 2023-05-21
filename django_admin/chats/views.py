from django.shortcuts import render
from authentication.models import Users
from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from rest_framework.response import Response


class UserListView(APIView):
    def get(self, request):
        response = Response()
        users = Users.objects.all()  # Retrieve all users from the Users model
        print('users')
        serializer = UserSerializer(users, many=True)  # Serialize the users if needed
        return Response(serializer.data)  # Return the serialized data as the API response

