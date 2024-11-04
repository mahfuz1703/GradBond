from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import alumniProfile, studentProfile
from core.views import home
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(home)
    
    if request.method == 'POST':
        userType = request.POST['userType']
        fullname = request.POST['fullname']
        university = request.POST['university']
        student_id = request.POST['student_id']
        email = request.POST['email']
        if userType == 'alumni':
            graduation_year = request.POST['graduation_year']
            company = request.POST['company']
            job_title = request.POST['job_title']
            linkedin = request.POST['linkedin']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if not email or not pass1 or not pass2:
            messages.warning(request, 'Please fill in all the fields.')
            return redirect('signup')
        
        if pass1 != pass2:
            messages.warning(request, 'Passwords do not match.')
            return redirect('signup')
        elif len(pass1) < 8:
            messages.warning(request, 'Password must be at least 8 characters long.')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists.')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=email, email=email, password=pass1)
            user.first_name = fullname
            user.save()

            if userType == 'alumni':
                alumni = alumniProfile(user=user, full_name=fullname, university=university, student_id=student_id, email=email, graduation_year=graduation_year, company=company, job_title=job_title, linkedin=linkedin)
                alumni.save()
            elif userType == 'student':
                student = studentProfile(user=user, full_name=fullname, university=university, student_id=student_id, email=email)
                student.save()
            
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('signin')
    return render(request, 'authentication/signup.html')

def signin(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(home)
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        if not email or not password:
            messages.warning(request, 'Please fill in all the fields.')
            return redirect('signin')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect(home)
        else:
            messages.warning(request, 'Invalid credentials.')
            return redirect('signin')
    return render(request, 'authentication/login.html')

def signout(request):
    logout(request)
    return redirect(signin)
