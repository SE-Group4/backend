from django.urls import path, re_path
from chat.views import MessageList

app_name = 'chat'

urlpatterns = [
    re_path('^(?P<room>[^/]+)/$', MessageList.as_view()),
]
