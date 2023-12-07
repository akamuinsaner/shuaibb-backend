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


    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        for tag in self.initial_data.get('tags'):
            tags.append(SampleLabel.objects.get(pk=tag.get('id')))
        sample = Sample.objects.create(**validated_data)
        user = User.objects.get(pk=self.initial_data.get('user_id'))
        sample.tags.set(tags)
        sample.user = user
        return sample

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for tag in self.initial_data.get('tags'):
            tags.append(SampleLabel.objects.get(pk=tag.get('id')))
        instance.tags.set(tags)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


