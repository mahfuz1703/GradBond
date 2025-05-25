from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from authentication.models import alumniProfile, studentProfile
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.formats import date_format
from django.conf import settings
from django.contrib.auth import authenticate, login
import json
import jwt
from .jwt_required import jwt_required


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

@csrf_exempt
def UserSignup(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 400,
            'message': 'You are already logged in.',
            'redirect': '/api/profile/'
        }, status=400)

    if request.method != 'POST':
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
        }, status=400)

    try:
        body = json.loads(request.body)
        userType = body.get('userType')
        email = body.get('email')

        pass1 = body.get('pass1')
        pass2 = body.get('pass2')
    except Exception as e:
        return JsonResponse({'status': 400, 'message': 'Invalid JSON'}, status=400)
    if not email or not pass1 or not pass2:
        return JsonResponse({'status': 400, 'message': 'Please fill in all the fields.'}, status=400)
    if pass1 != pass2:
        return JsonResponse({'status': 400, 'message': 'Passwords do not match.'}, status=400)
    elif len(pass1) < 8:
        return JsonResponse({'status': 400, 'message': 'Password must be at least 8 characters long.'}, status=400)
    elif User.objects.filter(email=email).exists():
        return JsonResponse({'status': 400, 'message': 'Email already exists.'}, status=400)
    else:
        user = User.objects.create_user(username=email, email=email, password=pass1)
        user.save()

        if userType == 'alumni':
            alumni = alumniProfile(user=user, email=email)
            alumni.save()
        elif userType == 'student':
            student = studentProfile(user=user, email=email)
            student.save()
        
        return JsonResponse({
            'status': 200,
            'message': 'Account created successfully. Please login.',
            'redirect': '/api/login/'
        }, status=200)
    
def UserLogout(request):
    # Clear the JWT cookie
    response = JsonResponse({
        'status': 200,
        'message': 'Logged out successfully',
        'redirect': '/'
    }, status=200)

    # Set an expired date to invalidate the token cookie
    response.delete_cookie(
        key='token',
        path='/',             # Make sure the path matches where you set it
        domain=None,          # If you set a domain while creating, add it here too
        samesite='None',
    )
    return response

def eventsApi(request):
    if request.method != 'GET':
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
        }, status=400)

    try:
        current_date = timezone.now().date()
        upcoming_events = events.objects.filter(date__gte=current_date)

        if upcoming_events.exists():
            events_list = []
            for event in upcoming_events:
                events_list.append({
                    'id': event.id,
                    'name': event.title,
                    'description': event.description,
                    'date': event.date.strftime('%Y-%m-%d') if event.date else None,
                    'time': event.time.strftime('%H:%M') if event.time else None,
                    'registration_link': event.regLink,
                    'location': event.location,
                    'image_url': event.image.url if event.image and hasattr(event.image, 'url') else None,
                    'created_by': str(event.user) if event.user else None,
                })
            return JsonResponse({
                'status': 200,
                'events': events_list
            }, status=200)
        else:
            return JsonResponse({
                'status': 404,
                'message': 'No events found'
            }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 500,
            'message': f'Server error: {str(e)}'
        }, status=500)

def event_detailApi(request, id):
    try:
        event = events.objects.get(id=id)

        event_detail = {
            'id': event.id,
            'name': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d') if event.date else None,
            'time': event.time.strftime('%H:%M') if event.time else None,
            'registration_link': event.regLink,
            'location': event.location,
            'image_url': event.image.url if event.image and hasattr(event.image, 'url') else None,
            'created_by': event.user.first_name if event.user else None,
        }

        return JsonResponse({
            'status': 200,
            'event': event_detail
        }, status=200)

    except events.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': 'Event not found'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 500,
            'message': f'Server error: {str(e)}'
        }, status=500)

def jobsApi(request):
    if request.method != 'GET':
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
        }, status=400)

    # Get current timezone-aware datetime
    current_date = timezone.now()
    
    try:
        all_jobs = Jobs.objects.filter(deadline__gte=current_date)

        try:
            body = json.loads(request.body)
            job_types = body.get('job_types')
            titleCompany = body.get('titleCompany')
            
            if job_types:
                all_jobs = all_jobs.filter(jobType=job_types)
            if titleCompany:
                all_jobs = all_jobs.filter(title__icontains=titleCompany) | all_jobs.filter(company__icontains=titleCompany)

        except json.JSONDecodeError:
            pass  # If no body is sent or it's not JSON, skip filtering

        # Serialize queryset to JSON
        jobs_json = list(all_jobs.values())  # Or use serializers if needed

        if jobs_json:
            return JsonResponse({
                'status': 200,
                'jobs': jobs_json
            }, status=200)
        else:
            return JsonResponse({
                'status': 404,
                'message': 'No jobs found'
            }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 500,
            'message': str(e),
        }, status=500)
    

def job_detailApi(request, id):
    if request.method != 'GET':
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method. Use GET.'
        }, status=400)

    try:
        job = Jobs.objects.get(id=id)

        job_detail = {
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'description': job.description,
            'jobType': job.job_type,
            'deadline': date_format(job.deadline, 'c'),  # ISO 8601 format
        }

        return JsonResponse({
            'status': 200,
            'job': job_detail
        }, status=200)

    except Jobs.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': 'Job not found'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 500,
            'message': f'Unexpected error: {str(e)}'
        }, status=500)