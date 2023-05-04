from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ApiKeyModel


class APIKEYAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None
        my_key = ApiKeyModel.verify(api_key)
        if not my_key:
            raise AuthenticationFailed('Invalid API Key for the specified app')
        return (my_key.user, None)
