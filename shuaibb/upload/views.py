
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileUploadSerializer
from utils.funcTools import upload_to_cos
from shuaibb.settings import ENV_CONFIG
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
        file = request.data["file"]
        name, ext = os.path.splitext(file.name)
        name = "{id}{ext}".format(id=str(uuid.uuid4()), ext=ext)
        prefix='https://{Bucket}.cos.{Region}.myqcloud.com/'.format(
            Bucket=ENV_CONFIG.get('Bucket'),
            Region=ENV_CONFIG.get('Region'),
        ),
        upload_to_cos(file, name)
        response = {}
        response["url"] = '{prefix}{name}'.format(prefix=prefix, name=name)
        return Response(response, status=status.HTTP_201_CREATED)
