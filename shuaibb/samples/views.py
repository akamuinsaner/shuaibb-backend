from lib2to3.pgen2.parse import ParseError
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
from rest_framework.exceptions import (
    ParseError,
    NotFound,
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

class SampleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=SampleSerializer

    def get_object(self):
        return Sample.objects.get(pk=self.kwargs['id'])

sample_detail_view = SampleDetailView.as_view()


class SampleCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = SampleSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            raise ParseError(detail="参数错误")

sample_create_view = SampleCreateView.as_view()

class SampleUpdateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        data = request.data
        sample_id = data.get('id')
        sample = Sample.objects.get(pk=sample_id)
        if (sample is not None):
            serializer = SampleSerializer(data=data, instance=sample)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                print(serializer.errors, serializer.error_messages)
                raise ParseError('参数错误')
        else:
            raise NotFound()

sample_update_view = SampleUpdateView.as_view()


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

############ label end ###########



