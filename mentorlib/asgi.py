"""
ASGI config for mentorlib project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from mentorlib.apps.courses.routing import websocket_urlpatterns
from mentorlib.apps.users.routing import websocket_user_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mentorlib.settings")

django_asgi_app = get_asgi_application()

websockets_urls = [*websocket_urlpatterns, *websocket_user_urlpatterns]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websockets_urls))
        ),
    }
)
