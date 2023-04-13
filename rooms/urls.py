from django.urls import path
from .views import ChatRoomList

app_name = 'rooms'

urlpatterns = [
    path('chat_rooms/', ChatRoomList.as_view()),
]
