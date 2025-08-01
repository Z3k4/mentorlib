from django.urls import re_path

from . import consumers

websocket_user_urlpatterns = [
    re_path(
        r"ws/notifications/(?P<room_name>\w+)/$",
        consumers.NotificationConsumer.as_asgi(),
    ),
]
