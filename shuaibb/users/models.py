from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
# Create your models here.
class User(AbstractBaseUser):
    mobile = models.CharField(null=True, unique=True)
    email = models.EmailField(null=True, unique=True)
    username = models.CharField(null=True, unique=True)
    nickname = models.CharField(null=True, unique=True)
    avatar = models.CharField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.mobile or self.email

