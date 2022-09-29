from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel, BotModel, OrderModel

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ("username", "first_name", "last_name", "email", "mt5_login", "mt5_password", "mt5_server")


        
class OrderSerializer(ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"

class BotSerializer(ModelSerializer):
    orders = OrderSerializer(many=True)
    class Meta:
        model = BotModel
        fields = "__all__"

class ActiveUsersSerializer(ModelSerializer):
    bots =  BotSerializer(many=True)
    class Meta:
        model = CustomUserModel
        fields = ("id", "username", "mt5_login", "mt5_password", "mt5_server", "bots")