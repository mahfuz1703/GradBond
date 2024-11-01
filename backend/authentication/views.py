from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def signup(request):
    return render(request, 'authentication/signup.html')

def login(request):
    return render(request, 'authentication/login.html')
