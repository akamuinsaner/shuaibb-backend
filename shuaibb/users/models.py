import enum
from inspect import signature
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from rest_framework.exceptions import ValidationError
# Create your models here.
class User(AbstractBaseUser):
    admin = 0
    photographer = 1
    anonymous = -1
    ROLE = (
        (admin, 'admin'),
        (photographer, 'photographer'),
        (anonymous, 'anonymous')
    )
    mobile = models.CharField(null=True, unique=True, blank=True)
    email = models.EmailField(null=True, unique=True, blank=True)
    username = models.CharField(null=True, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role=models.IntegerField(choices=ROLE, default=-1)
    groups = models.ManyToManyField(Group, related_name="users")
    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS = []

    avatar = models.CharField(null=True)
    nickname = models.CharField(null=True, blank=True, max_length=20)
    signature = models.CharField(null=True, blank=True, max_length=50)
    region = models.CharField(null=True, blank=True, max_length=20)
    address = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)

    covers = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.mobile or self.email

    @property
    def show_name(self):
        return self.username or self.mobile or self.email

    class Meta:
        permissions = (

        )

    def clean(self) -> None:
        if (self.username == None and self.mobile == None and self.email == None):
            raise ValidationError('at leat one of username,mobile or email')

