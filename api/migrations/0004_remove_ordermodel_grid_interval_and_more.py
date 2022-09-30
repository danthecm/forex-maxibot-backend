# Generated by Django 4.1 on 2022-09-30 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_ordermodel_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='grid_interval',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='symbol',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='order_id',
            field=models.CharField(default='sdafsd134', max_length=100),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='price',
            field=models.DecimalField(decimal_places=4, default='0.0004', max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='take_profit',
            field=models.DecimalField(decimal_places=4, default='0.0004', max_digits=5),
        ),
    ]
