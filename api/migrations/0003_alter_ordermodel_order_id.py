# Generated by Django 4.1 on 2022-09-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_ordermodel_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='order_id',
            field=models.IntegerField(max_length=100),
        ),
    ]
