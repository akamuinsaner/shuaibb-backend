# Generated by Django 4.2.7 on 2023-11-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0004_sampletemplate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sampletemplate',
            name='custom_detail',
        ),
        migrations.AlterField(
            model_name='sampletemplate',
            name='negative_film_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sampletemplate',
            name='refine_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sampletemplate',
            name='shooting_scene_indoor_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sampletemplate',
            name='shooting_time',
            field=models.IntegerField(default=0),
        ),
    ]
