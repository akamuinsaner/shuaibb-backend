from dataclasses import field
from rest_framework import serializers
from users.serializers import UserSerializer
from samples.serializers import SampleSerializer
from customers.serializers import CustomerSerializer
from .models import Schedule

class ScheduleHistorySerializer(serializers.ModelSerializer):
    sample = SampleSerializer(many=False, read_only=True)
    sample_id = serializers.IntegerField(required=True)
    user = UserSerializer(many=False, read_only=True)
    history_user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    customer = CustomerSerializer(many=False, read_only=True)
    customer_id = serializers.IntegerField(required=True)
    executors=UserSerializer(read_only=True, many=True)
    class Meta:
        model = Schedule.history.model
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(many=False, read_only=True)
    sample_id = serializers.IntegerField(required=True)
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    customer = CustomerSerializer(many=False, read_only=True)
    customer_id = serializers.IntegerField(required=True)
    executors=UserSerializer(read_only=True, many=True)
    history=ScheduleHistorySerializer(many=True, read_only=True)
    class Meta:
        model = Schedule
        fields = '__all__'