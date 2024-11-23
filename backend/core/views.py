from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from GradBond import settings
from authentication.models import alumniProfile, studentProfile
from .models import events
from django.shortcuts import redirect
from django.contrib import messages
import os

# Create your views here.
def home(request):
    event = events.objects.all()[:4]
    return render(request, 'core/index.html', {'events': event})


def search_alumni(request):
    if request.method == 'GET':
        university = request.GET.get('university')
        dept = request.GET.get('dept')
        company = request.GET.get('company')
        job_title = request.GET.get('job_title')
        randomKey = request.GET.get('randomKey')
        
        alumni = alumniProfile.objects.all()
        
        if university:
            alumni = alumni.filter(university__icontains=university)
        
        if dept:
            alumni = alumni.filter(dept__icontains=dept)
        
        if company:
            alumni = alumni.filter(company__icontains=company)
        
        if job_title:
            alumni = alumni.filter(job_title__icontains=job_title)

        if randomKey:
            if alumni.filter(university__icontains=randomKey).exists():
                alumni = alumni.filter(university__icontains=randomKey)
            
            if alumni.filter(dept__icontains=randomKey).exists():
                alumni = alumni.filter(dept__icontains=randomKey)
            
            if alumni.filter(company__icontains=randomKey).exists():
                alumni = alumni.filter(company__icontains=randomKey)

            if alumni.filter(job_title__icontains=randomKey).exists():
                alumni = alumni.filter(job_title__icontains=randomKey)
        
        return render(request, 'core/alumni_list.html', {'alumni_list': alumni})
    return render(request, 'core/find_alumni.html')

def find_alumni(request):
    return render(request, 'core/find_alumni.html')
        

def gallery(request):
    return render(request, 'core/gallery.html')

def view_events(request):
    all_events = events.objects.all()
    return render(request, 'core/event.html', {'events': all_events})

def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('eventTitle')
        description = request.POST.get('eventDes')
        date = request.POST.get('eventDate')
        time = request.POST.get('eventTime')
        regLink = request.POST.get('eventRegLink')
        location = request.POST.get('eventLocation')
        image = request.FILES.get('eventImage')
        
        event = events(user=request.user, title=title, description=description, date=date, time=time, regLink=regLink ,location=location, image=image)
        event.save()
        messages.success(request, 'Event added successfully.')
        
        return redirect('profile')
    return render(request, 'core/create_event.html')

def edit_event(request, id):
    event = events.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('eventTitle')
        description = request.POST.get('eventDes')
        date = request.POST.get('eventDate')
        time = request.POST.get('eventTime')
        regLink = request.POST.get('eventRegLink')
        location = request.POST.get('eventLocation')
        
        if 'eventImage' in request.FILES:
            # Delete the old image
            if event.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, event.image.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save the new image
            event.image = request.FILES['eventImage']
        
        event.title = title
        event.description = description
        event.date = date
        event.time = time
        event.regLink = regLink
        event.location = location
        event.save()
        messages.success(request, 'Event updated successfully.')
        
        return redirect('profile')
    return render(request, 'core/edit_event.html', {'event': event})

def delete_event(request, id):
    event = events.objects.get(id=id)
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('profile')

def event_detail(request, id):
    event = events.objects.get(id=id)
    return render(request, 'core/event_details.html', {'event': event})

def alumni_list(request):
    return render(request, 'core/alumni_list.html')

def profile(request):
    user = request.user
    
    email = user.email

    my_event = events.objects.filter(user=user)

    isAlumni = False
    if user.is_superuser:
        details = User.objects.get(username=user)
        return render(request, 'core/user_profile.html', {'details': details})

    if alumniProfile.objects.filter(email=email).exists():
        details = alumniProfile.objects.get(user=user)
        isAlumni = True
        return render(request, 'core/user_profile.html', {'details': details, 'isAlumni': isAlumni, 'events': my_event})
    else:
        details = studentProfile.objects.get(user=user)
        return render(request, 'core/user_profile.html', {'details': details, 'events': my_event})
    

def update_profile(request):
    user = request.user
    email = user.email
    isAlumni = False
    if alumniProfile.objects.filter(email=email).exists():
        isAlumni = True
        details = alumniProfile.objects.get(user=user)
        if request.method == 'POST':
            details.full_name = request.POST.get('full_name')
            details.university = request.POST.get('university') 
            details.dept = request.POST.get('dept')
            details.student_id = request.POST.get('student_id')
            details.email = details.email
            details.graduation_year = request.POST.get('graduation_year')
            details.company = request.POST.get('company')
            details.job_title = request.POST.get('job_title')
            details.linkedin = request.POST.get('linkedin')
            user.first_name = details.full_name
            
            if 'image' in request.FILES:
                old_image_path = os.path.join(settings.MEDIA_ROOT, details.image.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
                details.image = request.FILES.get('image')
            details.save()
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        return render(request, 'core/update_profile.html', {'details': details, 'isAlumni': isAlumni})
    else:
        details = studentProfile.objects.get(user=user)
        if request.method == 'POST':
            details.full_name = request.POST.get('full_name')
            details.university = request.POST.get('university') 
            details.dept = request.POST.get('dept')
            details.student_id = request.POST.get('student_id')
            details.email = details.email
            if 'image' in request.FILES:
                old_image_path = os.path.join(settings.MEDIA_ROOT, details.image.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
                details.image = request.FILES.get('image')
            details.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        return render(request, 'core/update_profile.html', {'details': details, 'isAlumni': isAlumni})
    
    return render(request, 'core/update_profile.html')
