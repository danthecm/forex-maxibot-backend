from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel, BotModel, OrderModel

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ("username", "first_name", "last_name", "email", "mt5_login", "mt5_password", "mt5_server")

class ActiveUsersSerializer(ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ("id", "username", "mt5_login", "mt5_password", "mt5_server")

class BotSerializer(ModelSerializer):
    class Meta:
        model = BotModel
        fields = "__all__"
        
class OrderSerializer(ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"