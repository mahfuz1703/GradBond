import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def jwt_required(view_func):
    """
    Decorator to check if the user is authenticated with a valid JWT token from cookies.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        logger.info(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")
        token = request.COOKIES.get('token')  # Retrieve token from cookies
        if not token:
            return JsonResponse({
                'status': 401,
                'message': 'Token not provided in cookies',
                'redirect': '/api/login/'
            }, status=401)

        try:
            # Decode the token
            decoded_data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = decoded_data.get('user_id')

            if not user_id:
                raise jwt.InvalidTokenError("User ID not found in token")

            # Get the actual user instance
            user = User.objects.get(id=user_id)
            request.user = user

        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'status': 401,
                'message': 'Token has expired',
                'redirect': '/api/login/'
            }, status=401)
        except (jwt.InvalidTokenError, User.DoesNotExist) as e:
            logger.error(f"JWT Error: {str(e)}")
            return JsonResponse({
                'status': 401,
                'message': 'Invalid token or user not found',
                'redirect': '/api/login/'
            }, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
