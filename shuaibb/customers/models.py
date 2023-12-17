from django.db import models
from users.models import User

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=10, null=False, blank=False)
    phone=models.CharField(null=False, blank=False, unique=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="costomers")
    avatar=models.CharField(null=True, blank=True)
    desc=models.TextField(null=True, blank=True)