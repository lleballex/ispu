import jwt

from django.conf import settings


def encode_auth_token(user_id: int) -> str:
    return jwt.encode({
        'user_id': user_id
    }, settings.SECRET_KEY)


def decode_auth_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return None

    return payload['user_id']
