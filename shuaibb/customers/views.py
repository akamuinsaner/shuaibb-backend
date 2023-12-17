from urllib import response
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerSerializer
from .models import Customer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.db.models import Q
# Create your views here.

class CustomerListView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CustomerSerializer
    
    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        list = Customer.objects.filter(user=self.request.user)
        if keyword is not None:
            list = list.filter(Q(name__contains=keyword) | Q(phone__contains=keyword))
        return list

customer_list_view = CustomerListView.as_view()


class CustomerDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CustomerSerializer

    def get_object(self):
        return Customer.objects.get(pk=self.kwargs["id"])

customer_detail_view = CustomerDetailView.as_view()

class CustomerBatchDeleteView(CreateAPIView):
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ids = request.data.get('ids')
        Customer.objects.filter(id__in=ids).delete()
        return Response(ids, status=HTTP_200_OK)

customer_batch_delete_view = CustomerBatchDeleteView.as_view()



