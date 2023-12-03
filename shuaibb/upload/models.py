from django.db import models

# Create your models here.
class UploadFile(models.Model):
    file = models.FileField()
    update_at = models.DateTimeField(auto_now_add=True)

