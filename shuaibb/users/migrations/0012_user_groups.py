# Generated by Django 4.2.7 on 2023-12-17 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_permission_chinese_name'),
        ('users', '0011_remove_user_nickname_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='users', to='auth.group'),
        ),
    ]