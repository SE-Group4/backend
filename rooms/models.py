from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=200)
    profile = models.ImageField(upload_to='uploads/profile')
    description = models.TextField(null=False, default='No description available')
    participants = models.ManyToManyField('chat.User', related_name='rooms')
    links = models.ManyToManyField('chat.Links', related_name='room_link')
    media = models.ManyToManyField('chat.Media')
    files = models.ManyToManyField('chat.File')
    group_chat = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.TimeField(default=timezone.now)
    stop_time = models.TimeField(default=timezone.now)
    date = models.DateField(auto_now=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
