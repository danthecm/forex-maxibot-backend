from .models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKEYModel, User

class APIKEYAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY')
        print("The entered api key is", api_key)
        my_key = APIKEYModel.create()
        print(my_key.key, my_key.name, my_key.user)
        raise AuthenticationFailed('Username not found, for the specified app')