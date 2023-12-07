from urllib import response
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from pictures.serializers import PictureFolderSerializer, FolderUUIDSerializer, PictureInfoSerializer
from pictures.models import PictureFolder, FolderUUID, PictureInfo
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import uuid
import os
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK
)
# Create your views here.
prefix = 'https://wangshuai-1300661566.cos.ap-beijing.myqcloud.com/'

def formatPics(list, folder_uuid): 
    for obj in list:
        obj['url'] = '{prefix}{space}/{user_path}/{uuid_name}{ext}'.format(
        prefix=prefix,
        space='picture-space',
        user_path=getattr(folder_uuid, 'id'),
        uuid_name=obj['uuid_name'],
        ext=obj['ext']
    )
    return list

class PictureFolderListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureFolderSerializer

    def get_queryset(self):
        folders = PictureFolder.objects.filter(parent=None, user=self.request.user)
        return folders

    def perform_create(self, serializer):
        name = self.request.data.get('name')
        parent_id = self.request.data.get('parent_id')
        parent = None
        folder = serializer.save()
        folder.user = self.request.user
        if (parent_id is not None):
            parent = PictureFolder.objects.get(pk=parent_id)
            folder.parent = parent

picture_folder_list_view = PictureFolderListView.as_view()







class PictureFolderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureFolderSerializer

    def get_object(self):
        print(self.kwargs['id'])
        return PictureFolder.objects.get(pk=self.kwargs['id'])

picture_folder_detail_view = PictureFolderDetailView.as_view()








class PictureListView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureInfoSerializer

    def get_queryset(self):
        pictures = PictureInfo.objects.filter(user=self.request.user)
        return pictures

    def create(self, request, *args, **kwargs):
        folder_uuid = FolderUUID.objects.filter(user=request.user).first()
        if (folder_uuid is None):
            serializer = FolderUUIDSerializer(data={ "user_id": getattr(request.user, 'id')})
            serializer.is_valid()
            folder_uuid = serializer.save()
        queryset = self.get_queryset()
        folder_id = request.data.get("folder_id")
        pictures = queryset.filter(folder_id=folder_id)
        data = PictureInfoSerializer(pictures, many=True).data
        return Response(formatPics(data, folder_uuid), status=HTTP_200_OK)

picture_list_view = PictureListView.as_view()






class PictureInfoDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureInfoSerializer

    def get_object(self):
        return PictureInfo.objects.get(pk=self.kwargs['id'])

picture_info_detail_view = PictureInfoDetailView.as_view()





class PictureAndFolderSearchView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        folder_uuid = FolderUUID.objects.filter(user=request.user).first()
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        folders = PictureFolder.objects.filter(user=request.user)
        pictures = PictureInfo.objects.filter(user=request.user)
        if (name is not None):
            folders = folders.filter(name__contains=name)
            pictures = pictures.filter(name__contains=name)
        if (start_date is not None):
            folders = folders.filter(updated_at__gte=start_date)
            pictures = pictures.filter(updated_at__gte=start_date)
        if (end_date is not None):
            folders = folders.filter(updated_at__lte=end_date)
            pictures = pictures.filter(updated_at__lte=end_date)
        response = {
            'folders': PictureFolderSerializer(folders, many=True).data,
            'pictures': formatPics(PictureInfoSerializer(pictures, many=True).data, folder_uuid)
        }
        return Response(response, status=HTTP_200_OK)

picture_and_folder_search_view = PictureAndFolderSearchView.as_view()






class PictureAndFolderBatchDeleteView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        folder_ids = request.data.get("folder_ids")
        picture_ids = request.data.get("picture_ids")
        print(folder_ids, picture_ids)
        if (folder_ids is not None):
            folders = PictureFolder.objects.filter(id__in=folder_ids)
            print(folders)
            folders.delete()
        if (picture_ids is not None):
            pictures = PictureInfo.objects.filter(id__in=picture_ids)
            print(pictures)
            pictures.delete()
        return Response(None, status=HTTP_200_OK)

picture_and_folder_batch_delete_view = PictureAndFolderBatchDeleteView.as_view()



class PictureAndFolderBatchMoveView(CreateAPIView):
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        parent_id = request.data["parent_id"]
        folder_ids = request.data.get('folder_ids')
        picture_ids = request.data.get('picture_ids')
        try: 
            if (folder_ids is not None):
                PictureFolder.objects.filter(id__in=folder_ids).update(parent_id=parent_id)
            if (picture_ids is not None):
                PictureInfo.objects.filter(id__in=picture_ids).update(folder_id=parent_id)
            return Response(None, status=HTTP_200_OK)
        except Exception:
            raise Exception
        
picture_and_folder_batch_move_view = PictureAndFolderBatchMoveView.as_view()




class PictureCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureInfoSerializer

    def create(self, request, *args, **kwargs):
        config = CosConfig(
            Region="ap-beijing",
            SecretId="AKIDGJI9rIj5Xq5CBuc6SoBXrEdxGR5maKyW",
            SecretKey="Tr7JNOMMMEwbmrrOtTwMo7GNL6d3Nk4K",
            Token=None,
            Scheme='https'
        )
        client = CosS3Client(config)
        file = request.data["file"]
        folder_id = request.data.get("folder_id")
        size = request.data.get("size")
        width = request.data.get("width")
        height = request.data.get("height")
        user_id = getattr(request.user, 'id')
        folder_uuid = FolderUUID.objects.get(user=request.user)
        folder_uuid_serializer = FolderUUIDSerializer(folder_uuid).data
        user_path = folder_uuid_serializer["id"]
        name, ext = os.path.splitext(file.name)
        info_data = {
            'folder_id': folder_id,
            'user_id': user_id,
            'name': name,
            'ext': ext,
            'size': size,
            'width': width,
            'height': height
        }
        serializer = PictureInfoSerializer(data=info_data)
        if (serializer.is_valid()):
            serializer.save()
            response = client.put_object(
                Bucket = "wangshuai-1300661566",
                Body=request.data["file"],
                Key='{space}/{user_path}/{file_name}'.format(
                    space='picture-space',
                    user_path=user_path,
                    file_name='{uuid_name}{ext}'.format(uuid_name=serializer.data['uuid_name'], ext=ext)
                ),
            )
            if (response):
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                raise Exception('上传失败')
        else:
            raise serializer.errors


picture_create_view = PictureCreateView.as_view()

