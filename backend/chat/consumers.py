import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
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
                'sender_image_url': sender_image_url,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_image_url': event['sender_image_url'],
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
