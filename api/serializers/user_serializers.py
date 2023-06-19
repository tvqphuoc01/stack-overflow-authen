from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)