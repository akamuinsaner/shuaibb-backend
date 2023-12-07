from rest_framework import serializers
from pictures.models import PictureFolder, FolderUUID, PictureInfo;
from users.serializers import UserSerializer;
from rest_framework_recursive.fields import RecursiveField


class PictureFolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    children = RecursiveField(many=True, required=False)
    class Meta:
        model = PictureFolder
        fields= '__all__'

class FolderUUIDSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=True)
    class Meta:
        model = FolderUUID
        fields= '__all__'

class PictureInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)
    folder = PictureFolderSerializer(many=False, read_only=True)
    folder_id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = PictureInfo
        fields= '__all__'