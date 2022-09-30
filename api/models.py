from email.policy import default
from random import choices
from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUserModel(User):
    mt5_login = models.BigIntegerField()
    mt5_password = models.CharField(max_length=225)
    mt5_server = models.CharField(max_length=200)
    
    def __str__(self):
        return self.username

class BotModel(models.Model):
    owner = models.ForeignKey(CustomUserModel, related_name="bots", on_delete=models.CASCADE)
    symbol = models.CharField(max_length=200)
    volume = models.DecimalField(decimal_places=2, max_digits=4)
    grid_interval = models.IntegerField()
    take_profit = models.IntegerField()
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.symbol

class OrderModel(models.Model):
    bot = models.ForeignKey(BotModel, related_name="orders", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=4, max_digits=5)
    volume = models.DecimalField(decimal_places=2, max_digits=4)
    type = models.CharField(max_length=10, choices=(("buy", "buy"), ("sell", "sell")))
    take_profit = models.DecimalField(decimal_places=4, max_digits=5)
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.type
