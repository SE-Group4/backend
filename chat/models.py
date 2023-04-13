from django.db import models

from rooms.models import ChatRoom


class Message(models.Model):
    sender = models.CharField(max_length=255)
    text = models.TextField()
    room = models.ManyToManyField(ChatRoom)
    timestamp = models.DateTimeField(auto_now_add=True)


