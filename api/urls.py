from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BotViewSet, OrderViewSet, ActiveUsersViewSet

my_router = DefaultRouter()
my_router.register("user", UserViewSet, "user")
my_router.register("bot", BotViewSet, "bot")
my_router.register("order", OrderViewSet, "order")
my_router.register("active_users", ActiveUsersViewSet, "active_users")


urlpatterns = [
     path('', include(my_router.urls)),
]

