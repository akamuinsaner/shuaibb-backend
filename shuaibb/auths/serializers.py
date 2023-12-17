from dataclasses import field
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=ContentType

class PermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(many=False, read_only=True)
    class Meta:
        fields="__all__"
        model=Permission


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        fields="__all__"
        model=Group