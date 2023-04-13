from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
