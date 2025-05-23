from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatMessage
from django.contrib.auth.models import User
from .utils import get_room_name
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

def index(request):
    return JsonResponse({'message': 'Welcome to the chat application!'})

@login_required
def chat_with_user(request, user_id):
    current_user = request.user
    selected_user = get_object_or_404(User, id=user_id)

    

    room_name = get_room_name(current_user, selected_user)
    messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')

    # Get chat users for sidebar
    chat_user_ids = ChatMessage.objects.filter(
        Q(sender=current_user) | Q(receiver=current_user)
    ).values_list('sender', 'receiver')

    user_ids = set()
    for s, r in chat_user_ids:
        if s != current_user.id:
            user_ids.add(s)
        if r != current_user.id:
            user_ids.add(r)

    users = User.objects.filter(id__in=user_ids)

    is_new_chat = not messages.exists()

    return render(request, 'chatting/chat.html', {
        'room_name': room_name,
        'messagess': messages,
        'selected_user': selected_user,
        'users': users,
        'is_new_chat': is_new_chat,
    })

@login_required
def chat_home(request):
    current_user = request.user

    chat_user_ids = ChatMessage.objects.filter(
        Q(sender=current_user) | Q(receiver=current_user)
    ).values_list('sender', 'receiver')

    user_ids = set()
    for s, r in chat_user_ids:
        if s != current_user.id:
            user_ids.add(s)
        if r != current_user.id:
            user_ids.add(r)

    users = User.objects.filter(id__in=user_ids)
    # Optionally, redirect to first chat if exists
    if users.exists():
        return redirect('chat_with_user', user_id=users.first().id)

    return render(request, 'chatting/chat.html', {
        'users': users,
        'selected_user': None,
        'messages': [],
        'room_name': None,
    })

@login_required
def chat_history(request, username):
    """Return chat history with a specific user in JSON format."""
    other_user = get_object_or_404(User, username=username)
    room_name = get_room_name(request.user, other_user)
    messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')

    message_data = [
        {
            'sender': msg.sender.username,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M')
        } for msg in messages
    ]

    return JsonResponse({'messagess': message_data})