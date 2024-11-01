from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'core/index.html')


def find_alumni(request):
    return render(request, 'core/find_alumni.html')

def gallery(request):
    return render(request, 'core/gallery.html')

def events(request):
    return render(request, 'core/event.html')

def alumni_list(request):
    return render(request, 'core/alumni_list.html')