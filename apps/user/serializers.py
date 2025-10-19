

from django.contrib.auth.models import User
from rest_framework import serializers
from .tasks import send_notify_have_new_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'username', 'email']
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        send_notify_have_new_user.delay(user.username, user.email)
        return user