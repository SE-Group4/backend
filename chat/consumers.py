# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        self.device_id = self.scope['client'][0]
        await self.channel_layer.group_add(f"user-{self.user.id}", self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        # leave room
        await self.channel_layer.group_discard(f"user-{self.user.id}", self.channel_name)
        await self.channel_layer.group_add(
            f"user-{self.user.id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user-{self.user.id}",
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


        if group_id:
            await self.send_group_message(message, group_id)
        elif recipient_id:
            await self.send_private_message(message, recipient_id)

    async def send_group_message(self, message, group_id):
        group_name = f"group-{group_id}"
        await self.channel_layer.group_send(
            group_name,
            {
                'type': 'group.message',
                'message': message,
                'username': self.user.username
            }
        )

    async def send_private_message(self, message, recipient_id):
        recipient_name = f"user-{recipient_id}"
        sender_name = f"user-{self.user.id}"
        await self.channel_layer.send(
            recipient_name,
            {
                'type': 'private.message',
                'message': message,
                'username': self.user.username,
                'sender_id': self.user.id,
                'recipient_id': recipient_id
            }
        )

    async def group_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def private_message(self, event):
        message = event['message']
        username = event['username']
        sender_id = event['sender_id']
        recipient_id = event['recipient_id']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sender_id': sender_id,
            'recipient_id': recipient_id
        }))
