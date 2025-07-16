from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfileModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        fields = ['username', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ProfileModel
        fields = ['id', 'user', 'Gender', 'Credit']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        profile, _ = ProfileModel.objects.get_or_create(user=user)
        token['role'] = profile.role
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        profile, _ = ProfileModel.objects.get_or_create(user=self.user)
        refresh = self.get_token(self.user)
        refresh['role'] = profile.role
        data['refresh'] = str(refresh)
        data['access']  = str(refresh.access_token)

        data['role'] = profile.role

        return data