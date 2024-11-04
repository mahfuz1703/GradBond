from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('find-alumni/', views.find_alumni, name='find-alumni'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('alumni-list/', views.alumni_list, name='alumni-list'),
    path('profile/', views.profile, name='profile'),

]