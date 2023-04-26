import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Room, RoomMessage


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.user = self.scope["user"]
        self.device_id = self.scope['client'][0]
        await self.channel_layer.group_add(f"user-{self.user.id}", self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        # leave room
        await self.channel_layer.group_discard(f"user-{self.user.id}", self.channel_name)

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

        group_id = data.get('group_id')
        recipient_id = data.get('recipient_id')

        # check if the message was sent by the user or the recipient
        sender_id = self.user.id
        is_sender = data.get('sender_id') == sender_id if data.get('sender_id') else True
        recipient = recipient_id == sender_id

        if group_id:
            await self.send_group_message(message, group_id)
        elif recipient_id:
            await self.send_private_message(message, recipient_id, is_sender, recipient)

    async def send_group_message(self, message, group_id):
        group_name = f"group-{group_id}"
        await self.channel_layer.group_send(group_name, {
            'type': 'group.message',
            'message': message,
            'username': self.user.username
        })

    async def send_private_message(self, message, recipient_id, is_sender, recipient):
        recipient_name = f"user-{recipient_id}"
        sender_name = f"user-{self.user.id}"
        from_device = "sender" if is_sender else "recipient"
        await self.channel_layer.group_send(recipient_name, {
            'type': 'private.message',
            'message': message,
            'username': self.user.username,
            'sender_id': self.user.id,
            'recipient_id': recipient_id,
            "from_device": from_device
        })




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
