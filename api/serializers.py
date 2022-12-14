from rest_framework import serializers
from .models import User, BotModel, OrderModel, TradeProfile


class TradeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeProfile
        fields = "__all__"

class SendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserSerializer(serializers.ModelSerializer):
    trade_profile = TradeProfileSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ("password", "is_staff", "is_superuser", "verification_code")

class RegisteriatonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"

class BotSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = BotModel
        fields = "__all__"

class ActiveUsersSerializer(serializers.ModelSerializer):
    trade_profile = TradeProfileSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ("password",)
        

class VerifySerializer(serializers.Serializer):
    code = serializers.IntegerField()
