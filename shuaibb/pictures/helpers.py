from .models import PictureInfo
from django.db.models import Sum
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from dotenv import dotenv_values

config = {
    **dotenv_values(".env.txcloud")
}

class Helpers():
    prefix = 'https://{Bucket}.cos.{Region}.myqcloud.com/'.format(Bucket=config.get('Bucket'), Region=config.get('Region'))
    @staticmethod 
    def size_check(user, size):
        total_size = PictureInfo.objects.filter(user=user).aggregate(Sum("size"))
        if (total_size["size__sum"] != None and (total_size["size__sum"] + int(size) > 2 * 1024 * 1024)):
            raise Exception('size exceed')
            

    @staticmethod 
    def formatPics(list, folder_uuid): 
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
        Bucket = config.pop("Bucket")
        config = CosConfig(
            **config,
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
        return response