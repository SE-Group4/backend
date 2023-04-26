import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Room, RoomMessage


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = await self.get_group(self.group_id)

        await self.channel_layer.group_add(
            self.group.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if message:
            user = self.scope['user']
            group_message = await self.create_group_message(user, message, self.group)
            group_message_data = await self.serialize_group_message(group_message)

            await self.channel_layer.group_send(
                self.group.group_name,
                {
                    'type': 'chat_message',
                    'message': group_message_data
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    @staticmethod
    async def get_group(group_id):
        try:
            group = await Room.objects.get(id=group_id)
            return group
        except Room.DoesNotExist:
            return None

    @staticmethod
    async def create_group_message(user, message, group):
        group_message = RoomMessage.objects.create(user=user, message=message, group=group)
        return group_message

    @staticmethod
    async def serialize_group_message(group_message):
        data = {
            'id': group_message.id,
            'user': group_message.user.username,
            'message': group_message.message,
            'created_at': str(group_message.created_at)
        }
        return data
