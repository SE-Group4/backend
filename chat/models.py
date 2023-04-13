from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False, default='No description available')
    participants = models.ManyToManyField(User, related_name='rooms')
    group_chat = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='private_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} in {self.room.name}: {self.content}'


class Links(models.Model):
    link_title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.link


class Media(models.Model):
    name = models.CharField(max_length=255)
    media = models.ImageField(upload_to='uploads/images')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
