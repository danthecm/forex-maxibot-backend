# Generated by Django 4.1.2 on 2022-10-26 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_botmodel_created_at_botmodel_modified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='price',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='take_profit',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
    ]
