from rest_framework import serializers
from users.models import User
from auths.serializers import GroupSerializer, PermissionSerializer

class UserSerializer(serializers.ModelSerializer):
    show_name=serializers.CharField(read_only=True, required=False)
    groups = GroupSerializer(read_only=True, required=False, many=True)
    user_permissions = PermissionSerializer(read_only=True, required=False)
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    groups = GroupSerializer(read_only=True, required=False, many=True)
    user_permissions = PermissionSerializer(read_only=True, required=False)
    class Meta:
        model = User
        fields = '__all__'