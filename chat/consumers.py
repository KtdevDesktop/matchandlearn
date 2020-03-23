from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Savechat
from django import db

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        db.connections.close_all()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        if not Savechat.objects.filter(name = self.room_name).exists():
            Savechat.objects.create(name=self.room_name, user1=self.room_name.split('_')[0], user2=self.room_name.split('_')[1])
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        db.connections.close_all()
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        db.connections.close_all()
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        db.connections.close_all()
        message = event['message']
        adddata = Savechat.objects.get(name=self.room_name)
        adddata.chat += message + "`~`~`~`~`~`"
        adddata.save()
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))