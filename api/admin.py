from django.contrib import admin
from .models import User, BotModel, OrderModel, TradeProfile, ApiKeyModel

# Register your models here.
admin.site.register((User, TradeProfile, BotModel, OrderModel, ApiKeyModel))
