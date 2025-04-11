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
        email = request.POST['email']

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
            user.save()

            if userType == 'alumni':
                alumni = alumniProfile(user=user, email=email)
                alumni.save()
            elif userType == 'student':
                student = studentProfile(user=user, email=email)
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
