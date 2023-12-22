from django.db import models
from users.models import User
from samples.models import Sample
from rest_framework.exceptions import ValidationError
from customers.models import Customer
from datetime import datetime, timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

class ScheduleHistoryAction(models.Model):
    action_text= models.CharField()

# Create your models here.
class Schedule(models.Model):
    CLOSED = -1
    UNPAID = 0
    DEPOSITPAID = 1
    ALLPAID = 2
    SHOOTINGDONE = 3
    ORDERFINISHED = 4
    PAYSTATUS = (     
        (CLOSED, '已关闭'),                           
        (UNPAID, '未付款'),                        
        (DEPOSITPAID, '已付定金'),                 
        (ALLPAID, '已付全款'),  
        (SHOOTINGDONE, '完成拍摄'),
        (ORDERFINISHED, '订单完成'),        
    ) 
    customer=models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="schedules")
    shoot_date=models.CharField(null=True, blank=True)
    start_time=models.CharField(null=True, blank=True)
    end_time=models.CharField(null=True, blank=True)
    date_settled=models.BooleanField(default=False)
    sample=models.ForeignKey(Sample, on_delete=models.DO_NOTHING, related_name="schedules")
    price=models.FloatField()
    deposit=models.FloatField()
    pay_status=models.IntegerField(choices=PAYSTATUS, default=UNPAID)
    location=models.CharField(null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="schedules")
    executors=models.ManyToManyField(User, related_name="orders")
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    _change_reason=models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    def clean(self) -> None:
        if self.date_settled == True and self.shoot_date is None:
            raise ValidationError('shoot_date is required')
        if self.date_settled == True and self.start_time is None:
            raise ValidationError('start_time is required')

