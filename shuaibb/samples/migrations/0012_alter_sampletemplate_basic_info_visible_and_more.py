# Generated by Django 4.2.7 on 2023-12-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0011_alter_sample_basic_info_visible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampletemplate',
            name='basic_info_visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='sampletemplate',
            name='costume_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
