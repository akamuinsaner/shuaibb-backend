from datetime import date, datetime
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .models import Schedule
from customers.models import Customer
from customers.serializers import CustomerSerializer
from .serializers import ScheduleSerializer, ScheduleHistorySerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from users.models import User

# Create your views here.
class ScheduleListView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ScheduleSerializer

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        list = Schedule.objects.filter(user=self.request.user)
        if (start_date is not None):
            list = list.filter(shoot_date__gte=start_date)
        if (end_date is not None):
            list = list.filter(shoot_date__lte=end_date)
        return list

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        if (customer_id is None):
            customer_name = request.data.get('customer_name')
            customer_phone = request.data.get('customer_phone')
            exist_one = Customer.objects.filter(phone=customer_phone).first()
            if (exist_one is not None):
                customer_serializer = CustomerSerializer(exist_one)
                customer_id = customer_serializer.data["id"]
            else :
                customer_serializer = CustomerSerializer(data={ 
                    'name': customer_name,
                    'phone': customer_phone,
                    'user_id': request.user.id
                })
                if (customer_serializer.is_valid()):
                    customer_serializer.save()
                    customer_id = customer_serializer.data["id"]
                else :
                    raise ValidationError(customer_serializer.errors)
        date_settled = request.data.get('date_settled')
        data = {
            "customer_id": customer_id,
            "sample_id": request.data.get('sample_id'),
            "price": request.data.get('price'),
            "deposit": request.data.get('deposit'),
            "pay_status": request.data.get("pay_status"),
            "location": request.data.get("location"),
            'user_id': request.user.id,
            "date_settled": date_settled,
            "_change_reason": request.data.get("_change_reason"),
        }
        if (date_settled is True):
            data["shoot_date"] = request.data.get('shoot_date')
            data["start_time"] = request.data.get('start_time')
            data["end_time"] = request.data.get('end_time')
        schedule_serializer = ScheduleSerializer(data=data)
        if (schedule_serializer.is_valid()):
            instance = schedule_serializer.save()
            executor_ids = request.data.get('executor_ids')
            if (executor_ids is not None):
                executors = User.objects.filter(id__in=executor_ids)
                instance.executors.set(executors)
            return Response(schedule_serializer.data, status=HTTP_201_CREATED)
        else:
            print(schedule_serializer.errors)
            raise ValidationError(schedule_serializer.errors)
            
schedule_list_view = ScheduleListView.as_view()

class ScheduleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ScheduleSerializer

    def get_object(self):
        return Schedule.objects.get(pk=self.kwargs["id"])

    def perform_update(self, serializer):
        instance = Schedule.objects.get(pk=self.kwargs["id"])
        serializer.save()
        executor_ids = self.request.data.get('executor_ids')
        if (executor_ids is not None):
            executors = User.objects.filter(id__in=executor_ids)
            instance.executors.set(executors)
        return Response(serializer.data, status=HTTP_201_CREATED)


schedule_detail_view = ScheduleDetailView.as_view()

class ScheduleHistoryView(ListAPIView):
    permission_classes=[IsAuthenticated]

    def list(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        schedule = Schedule.objects.get(pk=id)
        history = ScheduleHistorySerializer(schedule.history.all().order_by('history_date'), many=True).data
        return Response(history, status=HTTP_200_OK)

schedule_history_view = ScheduleHistoryView.as_view()

class ScheduleSearchView(CreateAPIView):
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        list = Schedule.objects.filter(user=request.user)
        customer_ids = request.data.get('customer_ids')
        if customer_ids != None and len(customer_ids) > 0:
            list = list.filter(customer__in=customer_ids)
        sample_ids = request.data.get('sample_ids')
        if sample_ids != None and len(sample_ids) > 0:
            list = list.filter(sample__in=sample_ids)
        pay_status = request.data.get('pay_status')
        if pay_status != None and len(pay_status) > 0:
            list = list.filter(pay_status__in=pay_status)
        executor_ids = request.data.get('executor_ids')
        if executor_ids != None and len(executor_ids) > 0:
            list = list.filter(executors__in=executor_ids).distinct()
        start_date = request.data.get('start_date')
        if start_date is not None:
            list = list.filter(shoot_date__gte=start_date)
        end_date = request.data.get('end_date')
        if end_date is not None:
            list = list.filter(shoot_date__lte=end_date)
        order = request.data.get('order')
        order_by = request.data.get('order_by')
        if (order_by is not None):
            order_by = "-{}".format(order_by) if order == 'desc' else order_by
            list = list.order_by(order_by)
        offset = request.data['offset']
        limit = request.data['limit']
        limitedData = list[offset * limit: (offset + 1) * limit]
        total = list.count()

        serializer = ScheduleSerializer(limitedData, many=True)
        response = {
            "data": serializer.data,
            "total": total,
            "offset": offset,
            "limit": limit
        }
        return Response(response, status=HTTP_200_OK)

schedule_search_view = ScheduleSearchView.as_view()

        

