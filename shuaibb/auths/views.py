from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission
from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from .serializers import GroupSerializer, PermissionSerializer, ContentTypeSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.apps.registry import Apps
# Create your views here.



class GroupListView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Group.objects.all()
    serializer_class=GroupSerializer

    def get_queryset(self):
        name = self.request.GET.get('name')
        list = Group.objects.filter()
        if (name is not None):
            list = list.filter(name__contains=name)
        return list

    @transaction.atomic
    def perform_create(self, serializer):
        permission_ids = self.request.data.get('permission_ids')
        group = serializer.save()
        if (permission_ids != None):
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)


group_list_view = GroupListView.as_view()

class GroupDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Group.objects.all()
    serializer_class=GroupSerializer

    def get_object(self):
        return Group.objects.get(pk=self.kwargs['id'])

    @transaction.atomic
    def perform_update(self, serializer):
        instance = Group.objects.get(pk=self.kwargs["id"])
        permission_ids = self.request.data.get('permission_ids')
        serializer.save()
        if (permission_ids != None):
            permissions = Permission.objects.filter(id__in=permission_ids)
            instance.permissions.clear()
            instance.permissions.set(permissions)

group_detail_view = GroupDetailView.as_view()

class GroupBatchDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ids = request.data["ids"]
        groups = Group.objects.filter(id__in=ids)
        groups.delete()
        return Response(ids, status=HTTP_200_OK)

group_batch_delete_view = GroupBatchDeleteView.as_view()



class PermissionListView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Permission.objects.all()
    serializer_class=PermissionSerializer

    def get_queryset(self):
        name = self.request.GET.get('name')
        list = Permission.objects.filter()
        if (name is not None):
            list = list.filter(name__contains=name)
        return list


permission_list_view = PermissionListView.as_view()

class PermissionDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Permission.objects.all()
    serializer_class=PermissionSerializer

    def get_object(self):
        return Permission.objects.get(pk=self.kwargs['id'])
        

permission_detail_view = PermissionDetailView.as_view()

class PermissionBatchDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ids = request.data["ids"]
        Permission.objects.filter(id__in=ids).delete()
        return Response(ids, status=HTTP_200_OK)

permission_batch_delete_view = PermissionBatchDeleteView.as_view()

class ContentTypeListView(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ContentTypeSerializer
    queryset=ContentType.objects.all()

content_type_list_view = ContentTypeListView.as_view()







