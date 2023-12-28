from .models import (
    Sample,
    SampleLabel,
    SampleTemplate
)
from .serializers import (
    SampleSerializer,
    SampleTemplateSerializer,
    SampleLabelSerializer
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK
)
from users.models import User;
from users.serializers import UserSerializer;
from rest_framework.exceptions import (
    ValidationError
)


class SampleDraftRetriveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            sample = Sample.objects.get(user=user, is_draft=True)
            data = SampleSerializer(sample).data
            return Response(data, status=HTTP_200_OK)
        except:
            return Response(None, status=HTTP_200_OK)



sample_draft_retrive_view = SampleDraftRetriveView.as_view()


class SampleCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        data = request.data
        tag_ids = self.request.data.get('tag_ids', [])
        tags = SampleLabel.objects.filter(id__in=tag_ids)
        serializer = SampleSerializer(data=data)
        if (serializer.is_valid()):
            instance = serializer.save()
            instance.tags.set(tags)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            raise ValidationError(serializer.error_messages)

sample_create_view = SampleCreateView.as_view()

class SampleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=SampleSerializer

    def get_object(self):
        return Sample.objects.get(pk=self.kwargs['id'])

    def perform_update(self, serializer):
        instance = Sample.objects.get(pk=self.kwargs['id'])
        serializer.save()
        tag_ids = self.request.data.get('tag_ids', [])
        tags = SampleLabel.objects.filter(id__in=tag_ids)
        instance.tags.set(tags)
        return Response(serializer.data, status=HTTP_200_OK)
        

sample_detail_view = SampleDetailView.as_view()


class SampleListView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        offset = request.data["offset"]
        limit = request.data["limit"]
        order = request.data.get('order')
        order_by = request.data.get('order_by')
        name = request.data.get('name')
        tag_ids = request.data.get('tag_ids')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        samples = Sample.objects.filter(
            is_draft=False,
            user=request.user,
        )
        if (name is not None):
            samples = samples.filter(name__contains=name)
        if (tag_ids is not None and len(tag_ids) > 0):
            samples = samples.filter(tags__in=tag_ids)
        if (order_by is not None):
            order_by = "-{}".format(order_by) if order == 'desc' else order_by
            samples = samples.order_by(order_by)
        if (start_date is not None):
            samples = samples.filter(created_at__gte=start_date)
        if (end_date is not None):
            samples = samples.filter(created_at__lte=end_date)
        limitedData = samples[offset * limit: (offset + 1) * limit]
        total = samples.count()

        serializer = SampleSerializer(limitedData, many=True)
        response = {
            "data": serializer.data,
            "total": total,
            "offset": offset,
            "limit": limit
        }
        return Response(response, status=HTTP_200_OK)

sample_list_view = SampleListView.as_view()


class SampeBatchDeleteView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        ids = request.data["ids"]
        Sample.objects.filter(id__in=ids).delete()
        return Response(ids, status=HTTP_200_OK)

sample_batch_delete_view = SampeBatchDeleteView.as_view()







######### template start ##########
class SampleTemplateListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SampleTemplateSerializer

    def get_queryset(self):
        return SampleTemplate.objects.all().filter(user = self.request.user)

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        if (queryset.count() >= 10):
            raise ValidationError('模板数量已达上限')
        serializer.save()

sample_template_list_view = SampleTemplateListView.as_view()

class SampleTemplateDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SampleTemplateSerializer

    def get_object(self):
        return SampleTemplate.objects.get(pk=self.kwargs['id'])

sample_template_detail_view = SampleTemplateDetailView.as_view()

######### template end ##########
    
############ label start ############
class SampleLabelList(ListCreateAPIView):
    queryset = SampleLabel.objects.all()
    serializer_class = SampleLabelSerializer
    permission_classes=[IsAuthenticated]


sample_label_list_view = SampleLabelList.as_view()

class SampleLabelDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = SampleLabelSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return SampleLabel.objects.get(pk=self.kwargs['id'])

    def perform_update(self, serializer):
        parent_id = self.request.data['parent_id']
        id = self.kwargs["id"]
        parent = SampleLabel.objects.filter(id=parent_id).first()
        while parent != None:
            if parent.id == id:
                raise ValidationError('请更换父级标签')
            else:
                parent = parent.parent
        serializer.save()

sample_label_detail_view = SampleLabelDetail.as_view()


class SampleLabelSearch(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        list = SampleLabel.objects.all()
        if (name != None):
            list = list.filter(name__contains=name)
        offset = request.data["offset"]
        limit = request.data["limit"]
        list = list[offset * limit: (offset + 1) * limit]
        total = list.count()
        serializer = SampleLabelSerializer(list, many=True)
        response = {
            "data": serializer.data,
            "total": total,
            "offset": offset,
            "limit": limit
        }
        return Response(response, status=HTTP_200_OK)

sample_label_search_view = SampleLabelSearch.as_view()

############ label end ###########



