from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.decorators import api_view
from django.urls import reverse
from django.utils import timezone

from rooms.models import Room
from chat.models import RoomMessage, PrivateMessage, Schedule, Category
from chat.serializers import UserSerializer, RoomMessageSerializer, PrivateMessageSerializer


# tests for room views
class RoomMessageTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.room = Room.objects.create(name='Test Room')

    def test_messages_api(self):
        url = '/messages/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_message_api(self):
        url = '/send_message/'
        data = {
            'room_id': self.room.id,
            'author': self.user.id,
            'content': 'Test message'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RoomMessage.objects.count(), 1)
        self.assertEqual(RoomMessage.objects.get().content, 'Test message')


# rooms model tests
class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name='Test Room',
            profile='uploads/profile/test_room.jpg',
            description='A test room for unit tests.',
            group_chat=True,
            is_private=False
        )

    def test_room_name(self):
        self.assertEqual(str(self.room), 'Test Room')

    def test_room_default_settings(self):
        self.assertTrue(self.room.group_chat)
        self.assertFalse(self.room.is_private)


class ScheduleModelTest(TestCase):
    def setUp(self):
        self.schedule = Schedule.objects.create(
            name='Test Schedule',
            start_time=timezone.now().time(),
            stop_time=timezone.now().time(),
            date=timezone.now().date(),
            location='Test Location'
        )

    def test_schedule_name(self):
        self.assertEqual(str(self.schedule), 'Test Schedule')


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_name(self):
        self.assertEqual(str(self.category), 'Test Category')


# urls tests
class ChatAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_signup(self):
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_add_interests(self):
        url = reverse('add_interests', args=[self.user.id])
        data = {
            'interests': ['music', 'books', 'movies']
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['interests'], ['music', 'books', 'movies'])

    def test_rooms(self):
        url = reverse('rooms')
        self.client.force
