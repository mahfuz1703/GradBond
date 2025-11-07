from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('search-alumni', views.search_alumni, name='search_alumni'),
    path('find-alumni', views.find_alumni, name='find-alumni'),
    path('events', views.view_events, name='events'),
    path('alumni-list', views.alumni_list, name='alumni-list'),
    path('profile', views.profile, name='profile'),
    path('about/<int:id>', views.about_user, name='about'),
    path('add-event', views.add_event, name='add-event'),
    path('event-detail/<int:id>', views.event_detail, name='event-detail'),
    path('edit-event/<int:id>', views.edit_event, name='edit_event'),
    path('delete-event/<int:id>', views.delete_event, name='delete_event'),
    path('update-profile', views.update_profile, name='update_profile'),

    path('jobs', views.view_jobs, name='jobs'),
    path('post-job', views.create_job, name='create_job'),
    path('job-detail/<int:id>', views.job_detail, name='job_detail'),
    path('edit-job/<int:id>', views.edit_job, name='edit_job'),
    path('delete-job/<int:id>', views.delete_job, name='delete_job'),

    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('contributions-count/', views.contributions_count_api, name='contrib_count'),

    # University management (admin upload + listing)
    path('university/upload/', views.university_upload, name='university_upload'),
    path('universities/', views.university_list, name='university-list'),

]