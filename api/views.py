from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable, ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from datetime import datetime
import pytz

from .auth import APIKEYAuthentication
from .serializers import (
    User, BotModel, OrderModel,
    UserSerializer, BotSerializer,
    OrderSerializer, ActiveUsersSerializer,
    RegisteriatonSerializer, LoginSerializer,
    TradeProfileSerializer, TradeProfile,
    SendVerificationSerializer
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from helpers.send_mail import send_verification
from helpers.verification import generate_code
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import authenticate

# Create your views here.


class RegisterationViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = RegisteriatonSerializer

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
        verify_url, code = generate_code(base_url, user.id)
        user.verification_code = code
        name = user.get_full_name
        verification_email = send_verification(name=name,
                                               email=email, url=verify_url)
        print("email verification", verification_email)
        if verification_email != "success":
            return Response({"message": "An error occured while registering please try later"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        user.save()
        print(f"HEllo {email} Your verification_code is: ", code)
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
            raise NotAcceptable("Please verify your email to continue.")
        refresh = RefreshToken.for_user(user)
        user.last_login = datetime.now(pytz.utc)
        user.save()
        response = Response({
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
        })
        response.set_cookie(key="refresh_token", value=str(
            refresh), samesite="None", secure=True, httponly=True)
        return response


class LogoutViewSet(ViewSet):
    http_method_names = ["get"]

    def list(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                print("No token was sent", refresh_token)
                raise Exception
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            response = Response({"detail": "Successfully logged out"})
            response.delete_cookie("refresh_token")
            return response
        except Exception as e:
            print(e)
            raise ParseError("Invalid token")


class TokenRefreshViewSet(ViewSet, TokenRefreshView):
    http_method_names = ["get"]

    def list(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                raise Exception
            token = RefreshToken(token=refresh_token)
            response = Response({
                "access_token": str(token.access_token)
            })
            return response
        except Exception as e:
            print("There was an error", e)
            raise ParseError("Invalid Token")


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ("get", "put", "patch", "delete")
    authentication_classes = [JWTAuthentication, APIKEYAuthentication]
    permission_classes = [IsAuthenticated]


class ActiveUsersViewSet(ViewSet):
    authentication_classes = [JWTAuthentication, APIKEYAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        queryset = User.objects.filter(
            is_verified=True, trade_profile__isnull=False)
        serializer = ActiveUsersSerializer(queryset, many=True)
        return Response(serializer.data)


class SendVerificationViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = SendVerificationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = get_object_or_404(self.queryset, email=email)
        print("the found user is ", user)

        if user is None:
            return Response({"detail": "user with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        base_url = get_current_site(request).domain
        name = user.get_full_name
        verify_url, code = generate_code(base_url, user.id)
        user.verification_code = code
        verification_email = send_verification(name=name,
                                               email=email, url=verify_url)
        print("email verification", verification_email)

        if verification_email != "success":
            return Response({"message": "An error occured while registering please try later"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        user.save()
        return Response({"detail": "email successfully sent"}, status=status.HTTP_202_ACCEPTED)


class VerifyViewSet(ViewSet):
    queryset = User.objects.all()

    def retrieve(self, request, pk: None):
        # Handle the POST method and the create action
        code = request.query_params.get("code")
        if code is None:
            return Response({"message": "You must send a code parameter in your request"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(self.queryset, id=pk)
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
    authentication_classes = [JWTAuthentication, APIKEYAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = self.queryset.filter(owner=user.id)
        serializer = self.serializer_class(queryset, many=True)
        # print("Cookies refresh Token ", request.COOKIES.get("refresh_token"))
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication, APIKEYAuthentication]
    permission_classes = [IsAuthenticated]


class TradeProfileViewSet(ModelViewSet):
    queryset = TradeProfile.objects.all()
    serializer_class = TradeProfileSerializer
    authentication_classes = [JWTAuthentication, APIKEYAuthentication]
    permission_classes = [IsAuthenticated]
