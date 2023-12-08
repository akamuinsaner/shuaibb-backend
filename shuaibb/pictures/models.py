from django.db import models
from users.models import User
from samples.models import SampleLabel
import uuid

# Create your models here.
class PictureFolder(models.Model):
    name = models.CharField(unique=False, null=False, max_length=10)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self) -> str:
        return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parent', 'name', 'user'], name='32432432')
        ]

class FolderUUID(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class PictureInfo(models.Model):
    labels = models.ManyToManyField(SampleLabel, default=[], blank=True, null=True)
    name= models.CharField(null=False, blank=True)
    ext= models.CharField(null=False, blank=True, default='')
    uuid_name=models.UUIDField(default=uuid.uuid4, editable=False)
    size=models.BigIntegerField(null=True, blank=True)
    width=models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    folder=models.ForeignKey(PictureFolder, blank=True, null=True, related_name="pictures", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pictures")
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name', 'folder'], name='12323131')
        ]
        