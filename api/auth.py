from .models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKEYModel, User

class APIKEYAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY')
        my_key = APIKEYModel.verify(api_key)
        if not my_key:
            raise AuthenticationFailed('Invalid API Key for the specified app')
        return (my_key.user, None)