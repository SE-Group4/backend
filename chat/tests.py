from django.test import TestCase, RequestFactory
from django.utils import timezone
from .models import Interests, User, RoomMessage, PrivateMessage, Links, Media, File
from rooms.models import Room, Schedule
from rest_framework.test import APIClient
from rest_framework import status
from chat.views import send_message



# test chat models
class ModelsTestCase(TestCase):
    def setUp(self):
        self.interests = Interests.objects.create(name='test interest')
        self.schedule = Schedule.objects.create()
        self.user = User.objects.create(user_id=1, first_name='test', last_name='user', username='testuser', email='testuser@example.com', password='testpass', interests=self.interests, schedule=self.schedule, is_online=True)
        self.room = Room.objects.create(name='test room')
        self.room_message = RoomMessage.objects.create(content='test message', timestamp=timezone.now())
        self.room_message.room.add(self.room)
        self.room_message.author = self.user
        self.private_message = PrivateMessage.objects.create(sender=self.user, recipient=self.user, content='test private message', timestamp=timezone.now())
        self.link = Links.objects.create(link_title='test link', link='http://test.com', uploaded_at=timezone.now())
        self.media = Media.objects.create(name='test media', media='uploads/images/test.png', uploaded_at=timezone.now())
        self.file = File.objects.create(name='test file', file='uploads/files/test.txt', uploaded_at=timezone.now())

    def test_interests_str(self):
        self.assertEqual(str(self.interests), 'test interest')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_room_message_str(self):
        expected_str = f'{self.user.username} in {self.room.name}: {self.room_message.content}'
        self.assertEqual(str(self.room_message), expected_str)

    def test_private_message_str(self):
        expected_str = f'{self.private_message.sender.username} -> {self.private_message.recipient.username}: {self.private_message.content}'
        self.assertEqual(str(self.private_message), expected_str)

    def test_links_str(self):
        self.assertEqual(str(self.link), 'test link')

    def test_media_str(self):
        self.assertEqual(str(self.media), 'test media')

    def test_file_str(self):
        self.assertEqual(str(self.file), 'test file')

# chat message views test
class RoomMessageTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.room = Room.objects.create(name='Test Room')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.message = 'Test message content'
        self.data = {
            'room_id': self.room.id,
            'content': self.message,
        }
        
    def test_send_message(self):
        request = self.factory.post('/send_message/', data=self.data)
        request.user = self.user
        response = send_message(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(RoomMessage.objects.filter(room=self.room, author=self.user, content=self.message).exists())
