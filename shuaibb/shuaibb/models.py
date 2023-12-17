from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

Permission.add_to_class('chinese_name', models.CharField(max_length=10, null=True, blank=True))
