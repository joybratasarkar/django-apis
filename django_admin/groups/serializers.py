
from rest_framework import serializers
from .models import Server,Message


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['server_name']


        # fields = '__all__'
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender', 'Server']