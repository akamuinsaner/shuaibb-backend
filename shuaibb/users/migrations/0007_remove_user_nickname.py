# Generated by Django 4.2.7 on 2023-12-02 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_email_alter_user_mobile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
    ]
