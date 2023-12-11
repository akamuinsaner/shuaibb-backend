from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from pictures.serializers import PictureFolderSerializer, FolderUUIDSerializer, PictureInfoSerializer
from pictures.models import PictureFolder, FolderUUID, PictureInfo
from django.db.models import Sum
from rest_framework.views import APIView
from samples.models import SampleLabel
from .helpers import Helpers
from rest_framework.exceptions import ValidationError
import os
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK
)
# Create your views here

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
        return Response(Helpers.formatPics(data, folder_uuid), status=HTTP_200_OK)

picture_list_view = PictureListView.as_view()






class PictureInfoDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureInfoSerializer

    def get_object(self):
        return PictureInfo.objects.get(pk=self.kwargs['id'])

picture_info_detail_view = PictureInfoDetailView.as_view()


class PictureTotalSizeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_size = PictureInfo.objects.filter(user=request.user).aggregate(Sum("size"))
        return Response(total_size["size__sum"], status=HTTP_200_OK)

picture_total_size_view = PictureTotalSizeView.as_view()





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
            'pictures': Helpers.formatPics(PictureInfoSerializer(pictures, many=True).data, folder_uuid)
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
        size = request.data.get("size")
        Helpers.size_check(request.user, size)
        file = request.data["file"]
        folder_id = request.data.get("folder_id")
        width = request.data.get("width")
        height = request.data.get("height")
        label_ids = request.data.get("label_ids")
        user_id = getattr(request.user, 'id')
        folder_uuid = FolderUUID.objects.get(user=request.user)
        folder_uuid_serializer = FolderUUIDSerializer(folder_uuid).data
        user_path = folder_uuid_serializer["id"]
        name = request.data.get("name")
        ext = ''
        labels = []
        if (label_ids is not None and label_ids is not ''):
            labels = SampleLabel.objects.filter(id__in=label_ids.split(','))
        if (name is None):
            print(name)
            name, ext = os.path.splitext(file.name)
        else:
            name, ext = os.path.splitext(name)
        same_name_object = PictureInfo.objects.filter(name=name)
        if (same_name_object.count() > 0):
            name = '{name}_副本'.format(name=name)
        
        info_data = {
            'folder_id': folder_id,
            'user_id': user_id,
            'name': name,
            'ext': ext,
            'size': size,
            'width': width,
            'height': height,
            'labels': labels
        }
        serializer = PictureInfoSerializer(data=info_data)
        if (serializer.is_valid()):
            picture_info = serializer.save()
            picture_info.labels.set(labels)
            uuid_name = serializer.data['uuid_name']
            response = Helpers.upload(file=file, user_path=user_path, uuid_name=uuid_name, ext=ext)
            if (response):
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                raise Exception('上传失败')
        else:
            raise ValidationError(serializer.errors)


picture_create_view = PictureCreateView.as_view()


class PictureCoverView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PictureInfoSerializer

    def create(self, request, *args, **kwargs):
        id = request.data['id']
        file = request.data["file"]
        size = request.data.get("size")
        Helpers.size_check(request.user, size)
        label_ids = request.data.get("label_ids")
        width = request.data.get("width")
        height = request.data.get("height")
        folder_uuid = FolderUUID.objects.get(user=request.user)
        folder_uuid_serializer = FolderUUIDSerializer(folder_uuid).data
        user_path = folder_uuid_serializer["id"]
        origin_data = PictureInfo.objects.filter(id=id)
        labels = []
        if (label_ids is not None):
            labels = SampleLabel.objects.filter(id__in=label_ids.split(','))
        data = PictureInfoSerializer(origin_data.first(), many=False).data
        origin_data.update(
            size=size,
            width=width,
            height=height,
        )
        origin_data.first().labels.set(labels)
        response= Helpers.upload(file=file, user_path=user_path, uuid_name=data["uuid_name"], ext=data["ext"])
        return Response(id, status=HTTP_200_OK)

picture_cover_view = PictureCoverView.as_view()


