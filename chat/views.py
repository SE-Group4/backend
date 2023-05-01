import json

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rooms.models import Room
from .models import RoomMessage, PrivateMessage
from .serializers import UserSerializer, RoomMessageSerializer, PrivateMessageSerializer


@api_view(['GET'])
def messages(request):
    message = RoomMessage.objects.all()
    messages_serializer = RoomMessageSerializer(message)
    serialized_data = messages_serializer.data
    json_data = json.dumps(serialized_data)
    return Response({'messages': json_data})


@api_view(['POST'])
def send_message(request):
    serializer = RoomMessageSerializer(data=request.data)
    if serializer.is_valid():
        # Create a new RoomMessage object and save it to the database
        room = Room.objects.get(id=serializer.validated_data['room_id'])
        author = request.user
        content = serializer.validated_data['content']
        room_message = RoomMessage.objects.create(room=room, author=author, content=content)

        message_data = {
            'message': content,
            'author_name': author.name,
        }
        message_json = json.dumps(message_data)
        Room(room.name).send({'text': message_json})

        # Return the new RoomMessage object in the response
        return Response(RoomMessageSerializer(room_message).data)
    else:
        return Response(serializer.errors, status=400)

