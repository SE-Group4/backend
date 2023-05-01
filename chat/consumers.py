import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import User, RoomMessage
from rooms.models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author_id = text_data_json['author_id']

        # Save message to database
        room = Room.objects.get(name=self.room_name)
        author = User.objects.get(id=author_id)
        RoomMessage.objects.create(room=room, author=author, content=message)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author_name': author.name
            }
        )

    async def chat_message(self, event):
        message = event['message']
        author_name = event['author_name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author_name': author_name
        }))