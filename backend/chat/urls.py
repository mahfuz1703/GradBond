from django.urls import path
from . import views

urlpatterns = [
    path('chat/with/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('inbox/', views.chat_home, name='chat_home'),
    path('chat/history/<str:username>/', views.chat_history, name='chat_history'),
]
