from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from datetime import datetime

# Create your views here.
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
