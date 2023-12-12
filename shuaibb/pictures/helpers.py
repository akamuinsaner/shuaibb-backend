from sys import prefix
from .models import PictureInfo
from django.db.models import Sum
from dotenv import dotenv_values
from shuaibb.settings import ENV_CONFIG
from utils.funcTools import upload_to_cos



class Helpers():
    @staticmethod 
    def size_check(user, size):
        total_size = PictureInfo.objects.filter(user=user).aggregate(Sum("size"))
        if (total_size["size__sum"] != None and (total_size["size__sum"] + int(size) > 2 * 1024 * 1024)):
            raise Exception('size exceed')
            

    @staticmethod 
    def formatPics(list, folder_uuid): 
        for obj in list:
            obj['url'] = '{prefix}{space}/{user_path}/{uuid_name}{ext}'.format(
            prefix='https://{Bucket}.cos.{Region}.myqcloud.com/'.format(
                Bucket=ENV_CONFIG.get('Bucket'),
                Region=ENV_CONFIG.get('Region'),
            ),
            space='picture-space',
            user_path=getattr(folder_uuid, 'id'),
            uuid_name=obj['uuid_name'],
            ext=obj['ext']
        )
        return list


    @staticmethod
    def upload(file, user_path, uuid_name, ext):
        return upload_to_cos(file, '{space}/{user_path}/{file_name}'.format(
            space='picture-space',
            user_path=user_path,
            file_name='{uuid_name}{ext}'.format(uuid_name=uuid_name, ext=ext)
        ))