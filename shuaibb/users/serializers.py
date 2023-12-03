from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = '__all__'