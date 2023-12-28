from rest_framework import serializers
from users.serializers import UserSerializer
from rest_framework_recursive.fields import RecursiveField
from users.models import User
from .models import (
    Sample,
    SampleLabel,
    SampleTemplate
)


class SampleLabelSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    children = RecursiveField(many=True, required=False)
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


