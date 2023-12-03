from django.db import models
from users.models import User

# Create your models here.

class SampleLabel(models.Model):
    name = models.CharField(unique=True, null=False, max_length=10)

    def __str__(self) -> str:
        return self.name

class SampleTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sample_templates")

    name = models.CharField(null=False, max_length=20)
    basic_info_visible = models.BooleanField(default=True)
    costume_offer = models.BooleanField(default=False)
    costume_count = models.IntegerField(default=None)
    custom_costume_count = models.IntegerField(default=0)
    negative_film_count = models.IntegerField()
    nega_film_all_offer = models.BooleanField(default=True)
    shooting_time = models.IntegerField(default=None)
    custom_shooting_time = models.IntegerField(default=0)
    refine_count = models.IntegerField(default=0)
    shooting_indoor = models.BooleanField(default=True)
    shooting_scene_indoor_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

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
    prive_visible = models.BooleanField(default=True)
    deposit = models.FloatField(null=False)
    deposit_visible = models.BooleanField(default=True)

    # service fields
    basic_info_visible = models.BooleanField(default=True)
    costume_offer = models.BooleanField(default=False)
    costume_count = models.IntegerField(default=None)
    custom_costume_count = models.IntegerField(default=0)
    negative_film_count = models.IntegerField()
    nega_film_all_offer = models.BooleanField(default=True)
    shooting_time = models.IntegerField(default=None)
    custom_shooting_time = models.IntegerField(default=0)
    refine_count = models.IntegerField(default=0)
    shooting_indoor = models.BooleanField(default=True)
    shooting_scene_indoor_count = models.IntegerField(default=0)
    custom_detail = models.TextField()

    # extra fields
    public = models.BooleanField(default=True)
    tips = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique name for each person')
        ]



