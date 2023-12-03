
from urllib import response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileUploadSerializer
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
import uuid
import os



class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class FileUploadCosView(APIView):
    
    def post(self, request):
        config = CosConfig(
            Region="ap-beijing",
            SecretId="AKIDGJI9rIj5Xq5CBuc6SoBXrEdxGR5maKyW",
            SecretKey="Tr7JNOMMMEwbmrrOtTwMo7GNL6d3Nk4K",
            Token=None,
            Scheme='https'
        )
        client = CosS3Client(config)
        file = request.data["file"]
        name, ext = os.path.splitext(file.name)
        name = "{id}{ext}".format(id=str(uuid.uuid4()), ext=ext)
        prefix = 'https://wangshuai-1300661566.cos.ap-beijing.myqcloud.com/'
        print(name)
        client.put_object(
            Bucket = "wangshuai-1300661566",
            Body=request.data["file"],
            Key=name,
        )
        response = {}
        response["url"] = '{prefix}{name}'.format(prefix=prefix, name=name)
        return Response(response, status=status.HTTP_201_CREATED)
