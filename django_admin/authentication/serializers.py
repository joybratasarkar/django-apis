from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_name', 'email', 'password','google_id']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 3, 'required': True},
            # 'name': {'required': False},
            # 'email': {'required': False}
        }
    def create(self, validated_data):
        user = Users.objects.create(**validated_data)
        return self.to_representation(user)
    # def create(self, validated_data):
    #     print(validated_data)
    #     email = self.context.get('email')
    #     google_id = self.context.get('google_id')
    #     name = self.context.get('name')
    #     return 'instance'

# class AuthenticateUser(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['user_name', 'email', 'password','google_id']
#         extra_kwargs = {
#             'password': {'write_only': True, 'min_length': 3, 'required': False},
#             'user_name': {'required': False},
#             'email': {'required': False}
#         }

#     def create(self, validated_data):
#         print(validated_data)
#         email = self.context.get('email')
#         google_id = self.context.get('google_id')
#         name = self.context.get('name')
#         return 'instance'

class UserSerializerForMessage(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_name']

    def create(self, validated_data):
        self.user.user_name