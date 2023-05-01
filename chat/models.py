from django.db import models
from rooms.models import Room, Schedule
from django.utils import timezone


class Interests(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    interests = models.ForeignKey(Interests, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class RoomMessage(models.Model):
    room = models.ManyToManyField(Room, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author.name} in {self.room.name}: {self.content}'


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_private_message')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_private_message')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


class Links(models.Model):
    link_title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.link


class Media(models.Model):
    name = models.CharField(max_length=255)
    media = models.ImageField(upload_to='uploads/images')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/files')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
