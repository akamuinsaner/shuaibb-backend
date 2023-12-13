from django.db import models
from users.models import User
from samples.models import Sample
from rest_framework.exceptions import ValidationError
from customers.models import Customer
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Schedule(models.Model):
    PAYSTATUS = (                                    
        (0, '未付款'),                        
        (1, '已付定金'),                 
        (2, '已付全款')                
    ) 
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="schedules")
    shoot_date=models.CharField(null=True, blank=True)
    start_time=models.CharField(null=True, blank=True)
    end_time=models.CharField(null=True, blank=True)
    date_settled=models.BooleanField(default=False)
    sample=models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="schedules")
    price=models.FloatField()
    deposit=models.FloatField()
    pay_status=models.IntegerField(choices=PAYSTATUS, default=0)
    location=models.CharField(null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")

    def clean(self) -> None:
        if self.date_settled == True and self.shoot_date is None:
            raise ValidationError('shoot_date is required')
        if self.date_settled == True and self.start_time is None:
            raise ValidationError('start_time is required')

