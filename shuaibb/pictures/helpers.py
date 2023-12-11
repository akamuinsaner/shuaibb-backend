from .models import PictureInfo
from django.db.models import Sum
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

class Helpers():
    prefix = 'https://wangshuai-1300661566.cos.ap-beijing.myqcloud.com/'
    @staticmethod 
    def size_check(user, size):
        total_size = PictureInfo.objects.filter(user=user).aggregate(Sum("size"))
        if (total_size["size__sum"] + int(size) > 2 * 1024 * 1024):
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
        config = CosConfig(
            Region="ap-beijing",
            SecretId="AKIDGJI9rIj5Xq5CBuc6SoBXrEdxGR5maKyW",
            SecretKey="Tr7JNOMMMEwbmrrOtTwMo7GNL6d3Nk4K",
            Token=None,
            Scheme='https'
        )
        client = CosS3Client(config)
        response = client.put_object(
            Bucket = "wangshuai-1300661566",
            Body=file,
            Key='{space}/{user_path}/{file_name}'.format(
                space='picture-space',
                user_path=user_path,
                file_name='{uuid_name}{ext}'.format(uuid_name=uuid_name, ext=ext)
            ),
        )
        return response