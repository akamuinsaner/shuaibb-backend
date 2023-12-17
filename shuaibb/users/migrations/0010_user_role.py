# Generated by Django 4.2.7 on 2023-12-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'admin'), (1, 'manager'), (2, 'photographer')], default=-1),
        ),
    ]
