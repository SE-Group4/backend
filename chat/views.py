from django.shortcuts import render

from rest_framework import generics
from chat.models import Message
from chat.serializers import MessageSerializer

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

