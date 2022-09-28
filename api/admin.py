from django.contrib import admin
from .models import CustomUserModel, BotModel, OrderModel

# Register your models here.
admin.site.register((CustomUserModel, BotModel, OrderModel))