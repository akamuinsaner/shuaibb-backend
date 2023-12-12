from users.models import User
from pictures.models import PictureInfo, FolderUUID
from pictures.serializers import PictureInfoSerializer, FolderUUIDSerializer
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from utils.funcTools import delete_from_cos

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=PictureInfo)
def upload_pictures(sender, instance=None, created=False, **kwargs):
    if created:
        data = PictureInfoSerializer(instance).data


@receiver(pre_delete, sender=PictureInfo)
def delete_picture_info(sender, instance=None, created=False, **kwargs):
    picture_info_data = PictureInfoSerializer(instance).data
    folder_uuid = FolderUUID.objects.filter(user_id=picture_info_data["user_id"]).first()
    folder_uuid_data = FolderUUIDSerializer(folder_uuid).data
    user_path = folder_uuid_data["id"]
    uuid_name = picture_info_data["uuid_name"]
    ext = picture_info_data["ext"]
    delete_from_cos('{space}/{user_path}/{file_name}'.format(
        space='picture-space',
        user_path=user_path,
        file_name='{uuid_name}{ext}'.format(uuid_name=uuid_name, ext=ext)
    ))
