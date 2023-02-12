from .models import User
from .utils import decode_auth_token

from rest_framework.request import Request 
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token = request.META.get('HTTP_AUTH_TOKEN')

        if not token: return None

        user_id = decode_auth_token(token)

        if not user_id:
            raise AuthenticationFailed('Wrong auth token')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('Wrong auth token')

        return (user, None)
