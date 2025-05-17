from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login
import json
import jwt


# Create your views here.
@csrf_exempt
def UserLogin(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
        }, status=400)

    try:
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')
    except Exception as e:
        return JsonResponse({'status': 400, 'message': 'Invalid JSON'}, status=400)

    user = authenticate(username=email, password=password)

    if user is not None:
        login(request, user)

        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        response = JsonResponse({
            'status': 200,
            'message': 'Login successful',
            'token': token,
            'redirect': '/api/profile/'
        })

        response.set_cookie(
            'token',
            token,
            httponly=True,
            secure=True,           # Required for SameSite=None
            samesite='None'        # Allows cross-site cookies
        )        
        return response

    return JsonResponse({
        'status': 401,
        'message': 'Invalid credentials'
    }, status=401)


def eventsApi(request):
    current_date = datetime.now()
    all_events = events.objects.filter(date__gte=current_date)

    if all_events.exists():
        events_list = []
        for event in all_events:
            events_list.append({
                'id': event.id,
                'name': event.title,
                'description': event.description,
                'date': event.date.strftime('%Y-%m-%d'),
                'time': event.time.strftime('%H:%M'),
                'registration_link': event.regLink,
                'location': event.location,
                'image_url': event.image.url if event.image else None,
                'created_by': event.user.first_name if event.user else None,
            })
        return JsonResponse({
            'status': '200',
            'events': events_list
        }, status = 200)
    else:
        return JsonResponse({
            'status': '404',
            'message': 'No events found'
        }, status = 404)


def event_detailApi(request, id):
    event = events.objects.get(id=id)

    if event:
        event_detail = {
            'id': event.id,
            'name': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M'),
            'registration_link': event.regLink,
            'location': event.location,
            'image_url': event.image.url if event.image else None,
            'created_by': event.user.first_name if event.user else None,
        }
        return JsonResponse({
            'status': '200',
            'event': event_detail
            }, status=200)
    else:
        return JsonResponse({
            'status': '404',
            'message': 'Event not found'
        }, status=404)
