from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, BotViewSet, OrderViewSet, ActiveUsersViewSet, VerifyViewSet,
                    RegisterationViewSet, LoginViewSet, TradeProfileViewSet, SendVerificationViewSet, LogoutViewSet, TokenRefreshViewSet, ApiKeyViewSet)

my_router = DefaultRouter()
my_router.register("user", UserViewSet, "user")
my_router.register(r"verify", VerifyViewSet, basename="verify")
my_router.register("send-verification", SendVerificationViewSet,
                   basename="send verification")
my_router.register("register", RegisterationViewSet, basename="register")
my_router.register('login', LoginViewSet, basename='login')
my_router.register("logout", LogoutViewSet, basename='logout')
my_router.register("refresh", TokenRefreshViewSet, basename="refresh")
my_router.register("trade-profile", TradeProfileViewSet,
                   basename='trade profile')
my_router.register("bot", BotViewSet, "bot")
my_router.register("order", OrderViewSet, "order")
my_router.register("active-users", ActiveUsersViewSet, "active users")
my_router.register("api-key", ApiKeyViewSet, "api key")


urlpatterns = [
    path('', include(my_router.urls)),
]
