# Generated by Django 4.1.7 on 2024-07-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_user_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="botmodel",
            name="min_margin_level",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]