from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/v1/', include('chat.urls')),
    path('api/v1/', include('rooms.urls')),
    # path("admin/", admin.site.urls),
]
