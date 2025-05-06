from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.eventsApi, name='eventsApi'),
    path('event/<int:id>/', views.event_detailApi, name='event_detailApi'),

]