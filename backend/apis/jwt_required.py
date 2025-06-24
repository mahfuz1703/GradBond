import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def jwt_required(view_func):
    """
    Decorator for verifying DRF SimpleJWT Access Tokens.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning("Missing or malformed Authorization header.")
            return JsonResponse({
                'status': 401,
                'message': 'Authorization header missing or invalid',
                'redirect': '/api/login/',
            }, status=401)

        token = auth_header.split(' ')[1]

        try:
            access_token = AccessToken(token)  # Will validate exp, signature, etc.
            user_id = access_token.get('user_id')
            if not user_id:
                logger.error("user_id not found in access token.")
                return JsonResponse({
                    'status': 401,
                    'message': 'Invalid token',
                    'redirect': '/api/login/',
                }, status=401)

            user = User.objects.get(id=user_id)
            request.user = user

        except TokenError as e:
            logger.warning(f"Token error: {str(e)}")
            return JsonResponse({
                'status': 401,
                'message': 'Invalid or expired token',
                'redirect': '/api/login/',
            }, status=401)

        except User.DoesNotExist:
            logger.error(f"User with id {user_id} not found.")
            return JsonResponse({
                'status': 401,
                'message': 'User not found',
                'redirect': '/api/login/',
            }, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

