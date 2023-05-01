from rest_framework import serializers
from chat.models import RoomMessage, PrivateMessage, User, Interests


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = '__all__'


class RoomMessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = RoomMessage
        fields = ['id', 'author', 'content', 'timestamp']


class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']

