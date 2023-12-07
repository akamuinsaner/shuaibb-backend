# Generated by Django 4.2.7 on 2023-12-05 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0003_remove_picturefolder_name_unique'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='picturefolder',
            constraint=models.UniqueConstraint(fields=('parent_id', 'name'), name='name unique'),
        ),
    ]
