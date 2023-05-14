from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'password','google_id']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 3, 'required': True},
            # 'name': {'required': False},
            # 'email': {'required': False}
        }

    # def create(self, validated_data):
    #     print(validated_data)
    #     email = self.context.get('email')
    #     google_id = self.context.get('google_id')
    #     name = self.context.get('name')
    #     return 'instance'

class AuthenticateUser(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'password','google_id']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 3, 'required': False},
            'name': {'required': False},
            'email': {'required': False}
        }

    def create(self, validated_data):
        print(validated_data)
        email = self.context.get('email')
        google_id = self.context.get('google_id')
        name = self.context.get('name')
        return 'instance'