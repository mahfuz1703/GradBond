import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from .models import ChatMessage, Notification
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def create_notification(self, sender, receiver, message):
        # fetch user full name from alumniprofile or studentprofile
        if hasattr(sender, 'alumniprofile'):
            sender_full_name = sender.alumniprofile.full_name
        elif hasattr(sender, 'studentprofile'):
            sender_full_name = sender.studentprofile.full_name

        notification = Notification.objects.create(
            user=receiver,
            notification_type='chat',
            message=f"New message from {sender_full_name}", #get user full name
            link=f"/chat/with/{sender.id}"
        )
        return notification

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']
        receiver_username = data['receiver']

        # for notification
        sender = await self.get_user(sender_username)
        receiver = await self.get_user(receiver_username)
        notification = await self.create_notification(sender, receiver, message)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f"notifications_{receiver.id}",
            {
                "type": "send_notification",
                "notification": {
                    "id": notification.id,
                    "message": notification.message,
                    "type": notification.notification_type,
                    "link": notification.link,
                    "is_read": notification.is_read,
                    "created_at": str(notification.created_at),
                }
            }
        )

        # Save the message
        await self.save_message(sender_username, receiver_username, message, self.room_name)

        # Get sender image URL
        sender_image_url = await self.get_sender_image_url(sender_username)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'receiver': receiver_username,
                'timestamp': timezone.now().strftime('%b %d, %Y %I:%M %p'),
                'sender_image_url': sender_image_url if sender_image_url else '',
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_image_url': event['sender_image_url'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message, room_name):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message,
            room_name=room_name
        )

    @database_sync_to_async
    def get_sender_image_url(self, sender_username):
        try:
            user = User.objects.get(username=sender_username)
            if hasattr(user, 'alumniprofile') and user.alumniprofile.image:
                return user.alumniprofile.image.url
            elif hasattr(user, 'studentprofile') and user.studentprofile.image:
                return user.studentprofile.image.url
        except User.DoesNotExist:
            return ''
        return ''


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.scope['user'].id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # No need to handle incoming messages from client

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["notification"]))

    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(user=self.scope["user"], is_read=False).count()