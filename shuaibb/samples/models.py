from django.db import models
from users.models import User
from datetime import datetime
from rest_framework.exceptions import ValidationError

# Create your models here.

class SampleLabel(models.Model):
    name = models.CharField(unique=True, null=False, max_length=10)

    def __str__(self) -> str:
        return self.name

class SampleTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sample_templates")
    name = models.CharField(null=False, max_length=20)
    basic_info_visible = models.BooleanField(null=False, blank=False)
    costume_offer = models.BooleanField(null=False, blank=False)
    costume_count = models.IntegerField(default=None)
    negative_film_count = models.IntegerField(null=False, blank=False)
    nega_film_all_offer = models.BooleanField(null=False, blank=False)
    shooting_time = models.IntegerField(null=False, blank=False)
    refine_count = models.IntegerField(null=False, blank=False)
    shooting_indoor = models.BooleanField(null=False, blank=False)
    shooting_scene_indoor_count = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        if (self.costume_offer == True and self.costume_count == None):
            raise ValidationError('custome_count is required')
        if (self.shooting_indoor == True and self.shooting_scene_indoor_count == None):
            raise ValidationError('shooting_scene_indoor_count is required')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique template name for each person')
        ]


class Sample(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="samples")
    is_draft = models.BooleanField(default=True)

    # name fields
    name = models.CharField(null=False, max_length=30)
    desc = models.TextField(null=False, max_length=500)
    tags = models.ManyToManyField(SampleLabel)
    covers = models.TextField(max_length=1000000)
    details = models.TextField(max_length=1000000)

    # price fields
    price = models.FloatField(null=False)
    price_visible = models.BooleanField(null=False, blank=False)
    deposit = models.FloatField(null=False)
    deposit_visible = models.BooleanField(null=False, blank=False)

    # service fields
    basic_info_visible = models.BooleanField(null=False, blank=False)
    costume_offer = models.BooleanField(null=False, blank=False)
    costume_count = models.IntegerField(null=True, blank=True)
    negative_film_count = models.IntegerField(null=False, blank=False)
    nega_film_all_offer = models.BooleanField(null=False, blank=False)
    shooting_time = models.IntegerField(null=False, blank=False)
    refine_count = models.IntegerField(null=False, blank=False)
    shooting_indoor = models.BooleanField(null=False, blank=False)
    shooting_scene_indoor_count = models.IntegerField(null=True, blank=True)
    custom_detail = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    # extra fields
    public = models.BooleanField(null=False, blank=False)
    tips = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        if (self.costume_offer == True and self.costume_count == None):
            raise ValidationError('custome_count is required')
        if (self.shooting_indoor == True and self.shooting_scene_indoor_count == None):
            raise ValidationError('shooting_scene_indoor_count is required')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique name for each person')
        ]





