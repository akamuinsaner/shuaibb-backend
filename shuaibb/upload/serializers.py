from rest_framework import serializers
from upload.models import UploadFile


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'