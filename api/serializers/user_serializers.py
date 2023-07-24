from rest_framework import serializers
from api.models import User, Role


class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)

class RequestUserSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
