from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLogin, name='UserLogin'),
    path('logout/', views.UserLogout, name='UserLogout'),
    path('signup/', views.UserSignup, name='UserSignup'),

    path('events/', views.eventsApi, name='eventsApi'),
    path('event/<int:id>/', views.event_detailApi, name='event_detailApi'),

    path('jobs/', views.jobsApi, name='jobsApi'),
    path('job/<int:id>/', views.job_detailApi, name='job_detailApi'),

    path('find-alumni/', views.searchAlumniApi, name='findAlumniApi'),

    path('profile/', views.profileApi, name='profileApi'),

]