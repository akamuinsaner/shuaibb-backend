# Generated by Django 4.2.7 on 2023-12-14 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_nickname_alter_user_email_alter_user_mobile_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': ()},
        ),
    ]
