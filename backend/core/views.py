from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from authentication.models import alumniProfile, studentProfile
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'core/index.html')


def search_alumni(request):
    if request.method == 'GET':
        university = request.GET.get('university')
        dept = request.GET.get('dept')
        company = request.GET.get('company')
        job_title = request.GET.get('job_title')
        
        alumni = alumniProfile.objects.all()
        
        if university:
            alumni = alumni.filter(university__icontains=university)
        
        if dept:
            alumni = alumni.filter(dept__icontains=dept)
        
        if company:
            alumni = alumni.filter(company__icontains=company)
        
        if job_title:
            alumni = alumni.filter(job_title__icontains=job_title)
        
        return render(request, 'core/alumni_list.html', {'alumni_list': alumni})
    return render(request, 'core/find_alumni.html')

def find_alumni(request):
    return render(request, 'core/find_alumni.html')
        

def gallery(request):
    return render(request, 'core/gallery.html')

def events(request):
    return render(request, 'core/event.html')

def alumni_list(request):
    return render(request, 'core/alumni_list.html')

def profile(request):
    user = request.user
    
    email = user.email

    isAlumni = False
    if alumniProfile.objects.filter(email=email).exists():
        details = alumniProfile.objects.get(user=user)
        isAlumni = True
        return render(request, 'core/profile.html', {'details': details, 'isAlumni': isAlumni})
    else:
        details = studentProfile.objects.get(user=user)
        return render(request, 'core/profile.html', {'details': details})