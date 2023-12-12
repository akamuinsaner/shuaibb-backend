from sys import prefix
from .models import PictureInfo
from django.db.models import Sum
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from dotenv import dotenv_values
from shuaibb.settings import ENV_BASE_DIR


class Helpers():
    config = {**dotenv_values(ENV_BASE_DIR / ".env.txcloud")}
    @staticmethod 
    def size_check(user, size):
        total_size = PictureInfo.objects.filter(user=user).aggregate(Sum("size"))
        if (total_size["size__sum"] != None and (total_size["size__sum"] + int(size) > 2 * 1024 * 1024)):
            raise Exception('size exceed')
            

    @staticmethod 
    def formatPics(list, folder_uuid): 
        print(dotenv_values(".env.txcloud"))
        for obj in list:
            obj['url'] = '{prefix}{space}/{user_path}/{uuid_name}{ext}'.format(
            prefix=Helpers.prefix,
            space='picture-space',
            user_path=getattr(folder_uuid, 'id'),
            uuid_name=obj['uuid_name'],
            ext=obj['ext']
        )
        return list


    @staticmethod
    def upload(file, user_path, uuid_name, ext):
        Bucket = Helpers.config["Bucket"]
        print(Helpers.config)
        config = CosConfig(
            Region=Helpers.config["Region"],
            SecretId=Helpers.config["SecretId"],
            SecretKey=Helpers.config["SecretKey"],
            Token=Helpers.config["Token"],
            Scheme=Helpers.config["Scheme"]
        )
        client = CosS3Client(config)
        response = client.put_object(
            Bucket = Bucket,
            Body=file,
            Key='{space}/{user_path}/{file_name}'.format(
                space='picture-space',
                user_path=user_path,
                file_name='{uuid_name}{ext}'.format(uuid_name=uuid_name, ext=ext)
            ),
        )
        print(response)
        return response

Helpers.prefix = 'https://{Bucket}.cos.{Region}.myqcloud.com/'.format(
    Bucket=Helpers.config.get('Bucket'),
    Region=Helpers.config.get('Region'),
)