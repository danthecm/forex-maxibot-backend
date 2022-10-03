# Generated by Django 4.1 on 2022-10-03 06:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_ordermodel_created_at_ordermodel_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='botmodel',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='botmodel',
            name='modified_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
