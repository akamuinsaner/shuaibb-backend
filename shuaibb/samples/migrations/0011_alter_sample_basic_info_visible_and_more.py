# Generated by Django 4.2.7 on 2023-12-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0010_rename_prive_visible_sample_price_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='basic_info_visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='custom_detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='deposit_visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='price_visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='public',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='tips',
            field=models.TextField(blank=True, null=True),
        ),
    ]
