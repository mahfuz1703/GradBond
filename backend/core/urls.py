from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('search-alumni/', views.search_alumni, name='search_alumni'),
    path('find-alumni/', views.find_alumni, name='find-alumni'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.view_events, name='events'),
    path('alumni-list/', views.alumni_list, name='alumni-list'),
    path('profile/', views.profile, name='profile'),
    path('add-event/', views.add_event, name='add-event'),
    path('event-detail/<int:id>/', views.event_detail, name='event-detail'),
    path('edit-event/<int:id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:id>/', views.delete_event, name='delete_event'),
    path('update-profile/', views.update_profile, name='update_profile'),

]