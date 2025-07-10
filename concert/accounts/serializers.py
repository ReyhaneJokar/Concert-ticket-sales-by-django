from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfileModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ProfileModel
        fields = ['id', 'user', 'Gender', 'Credit']
