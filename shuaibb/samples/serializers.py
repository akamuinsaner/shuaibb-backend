from rest_framework import serializers
from users.serializers import UserSerializer
from users.models import User
from .models import (
    Sample,
    SampleLabel,
    SampleTemplate
)


class SampleLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleLabel
        fields= '__all__'

class SampleTemplateSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    class Meta:
        model = SampleTemplate
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    tags = SampleLabelSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    class Meta:
        model = Sample
        fields = '__all__'


