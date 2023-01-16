from .models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKEYAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('APP_KEY')
        print("The entered api key is", api_key)
        return super().authenticate(request)