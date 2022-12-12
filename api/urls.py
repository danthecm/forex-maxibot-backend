from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BotViewSet, OrderViewSet, ActiveUsersViewSet, VerifyViewSet, RegisterationViewSet, LoginViewSet, TradeProfileViewSet, SendVerificationViewSet

my_router = DefaultRouter()
my_router.register("user", UserViewSet, "user")
my_router.register(r"verify", VerifyViewSet, basename="verify")
my_router.register("send_verification", SendVerificationViewSet, basename="send_verification")
my_router.register("register", RegisterationViewSet, basename="register")
my_router.register('login', LoginViewSet, basename='login')
my_router.register("trade_profile", TradeProfileViewSet,
                   basename='trade_profile')
my_router.register("bot", BotViewSet, "bot")
my_router.register("order", OrderViewSet, "order")
my_router.register("active_users", ActiveUsersViewSet, "active_users")


urlpatterns = [
    path('', include(my_router.urls)),
]
