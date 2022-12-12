from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (
    User, BotModel, OrderModel,
    UserSerializer, BotSerializer, 
    OrderSerializer, ActiveUsersSerializer, 
    RegisteriatonSerializer, LoginSerializer,
    TradeProfileSerializer, TradeProfile,
    SendVerificationSerializer
)
from django.contrib.sites.shortcuts import get_current_site
from helpers.send_mail import send_verification
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import authenticate
import random
import string

# Create your views here.


class RegisterationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisteriatonSerializer
    http_method_names = ("post")

    def create(self, request):
        # Custom create logic
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        user = self.queryset.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        base_url = get_current_site(request).domain
        verificiation_code = ''.join(random.choices(string.digits, k=6))
        user.verification_code = verificiation_code
        verify_url = f"http://{base_url}/verify/{user.id}/?code={verificiation_code}"
        print(verify_url)
        name = user.get_full_name if user.get_full_name else "New User"
        verification_email = send_verification(name=name,
                                                    email=email, url=verify_url)
        print("email verification", verification_email)
        if verification_email != "success":
            return Response({"message": "An error occured while registering please try later"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        user.save()
        print(f"HEllo {email} Your verification_code is: ", verificiation_code)
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        response = {
            "user": UserSerializer(user).data,
            "access_token": str(access_token),
            "refresh_token": str(refresh_token)
        }
        return Response(response, status=status.HTTP_200_OK)



class LoginViewSet(ViewSet):
  serializer_class = LoginSerializer

  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
      raise AuthenticationFailed('Invalid username or password')
    
    elif user.is_verified is False:
        raise NotAcceptable("You must verify your account to login")

    refresh = RefreshToken.for_user(user)

    return Response({
        'user': UserSerializer(user).data,
      'refresh_token': str(refresh),
      'access_token': str(refresh.access_token),
    })



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ("get", "put", "patch", "delete")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ActiveUsersViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        queryset = User.objects.all()
        serializer = ActiveUsersSerializer(queryset, many=True)
        return Response(serializer.data)

class SendVerificationViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = SendVerificationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

class VerifyViewSet(ViewSet):
    queryset = User.objects.all()

    def retrieve(self, request, pk: None):
        # Handle the POST method and the create action
        code = request.query_params.get("code")
        if code is None:
            return Response({"message": "You must send a code parameter in your request"}, status=status.HTTP_400_BAD_REQUEST)
        user = self.queryset.filter(pk=pk).first()
        if user is None:
            return Response({"message": "User not Found"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_verified:
            return Response({"message": "Email Already Verified"}, status=status.HTTP_200_OK)
        code = int(code)
        verification_code = user.verification_code
        if code == verification_code:
            user.is_verified = True
            user.save()
            return Response({"message": "Email Verified Successfully"}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid Verification Code"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BotViewSet(ModelViewSet):
    queryset = BotModel.objects.all()
    serializer_class = BotSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class TradeProfileViewSet(ModelViewSet):
    queryset = TradeProfile.objects.all()
    serializer_class = TradeProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
