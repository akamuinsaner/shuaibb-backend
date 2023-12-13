from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    class Meta:
        model = Customer
        fields = '__all__'
