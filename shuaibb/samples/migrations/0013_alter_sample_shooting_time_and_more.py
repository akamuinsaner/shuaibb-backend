# Generated by Django 4.2.7 on 2023-12-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0012_alter_sampletemplate_basic_info_visible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='shooting_time',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='sampletemplate',
            name='shooting_time',
            field=models.FloatField(),
        ),
    ]
