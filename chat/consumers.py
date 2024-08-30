# chat/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatRoom, Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = self.scope["user"].id
        room_name = self.room_name

        # Save message to database
        room = ChatRoom.objects.get(name=room_name)
        user = User.objects.get(id=user_id)
        Message.objects.create(room=room, user=user, content=message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope["user"].username,
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))
