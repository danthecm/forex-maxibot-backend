# Generated by Django 4.1 on 2022-09-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_ordermodel_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='order_id',
            field=models.IntegerField(),
        ),
    ]
