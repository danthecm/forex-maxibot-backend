# Generated by Django 4.1.4 on 2023-01-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_botmodel_pip_margin_alter_ordermodel_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="botmodel",
            name="pip_margin",
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]