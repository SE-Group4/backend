from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/v1/', include('chat.urls', namespace='chat')),
    path('api/v1/', include('rooms.urls', namespace='rooms')),
    path("admin/", admin.site.urls),
]
