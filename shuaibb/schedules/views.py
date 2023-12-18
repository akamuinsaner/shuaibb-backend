from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Schedule
from customers.models import Customer
from customers.serializers import CustomerSerializer
from .serializers import ScheduleSerializer
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
            "date_settled": date_settled
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
            raise ValidationError(schedule_serializer.errors)
            
schedule_list_view = ScheduleListView.as_view()
        

