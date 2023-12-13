from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerSerializer
from .models import Customer
# Create your views here.

class CustomerListView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CustomerSerializer
    
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

customer_list_view = CustomerListView.as_view()



