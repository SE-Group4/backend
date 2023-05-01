from django.urls import path, re_path
from . import views

app_name = 'chat'


urlpatterns = [
    path('room-message/', views.messages),
    # path('chat/details/<int:id>', views.chat_details),
]
