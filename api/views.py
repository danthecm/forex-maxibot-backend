from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from .serializers import (
    CustomUserModel, BotModel, OrderModel,
    UserSerializer, BotSerializer, OrderSerializer,
    ActiveUsersSerializer)

# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = CustomUserModel.objects.all()
    serializer_class = UserSerializer


class ActiveUsersViewSet(ViewSet):

    def list(self, request):
        queryset = CustomUserModel.objects.all()
        serializer = ActiveUsersSerializer(queryset, many=True)
        return Response(serializer.data)


class BotViewSet(ModelViewSet):
    queryset = BotModel.objects.all()
    serializer_class = BotSerializer


class OrderViewSet(ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
