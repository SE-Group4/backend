from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # join room
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, code):
        # leave room
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        pass

    def receive(self, room_data):
        rooms_data_json = json.loads(room_data)
        room = rooms_data_json['room']

        self.send(room_data_sjon=json.dumps({'room': room}))
