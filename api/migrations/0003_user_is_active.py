# Generated by Django 4.1.7 on 2024-04-17 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_botmodel_ratio"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
