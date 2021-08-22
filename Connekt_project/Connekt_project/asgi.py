"""
ASGI config for Connekt_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from firstApp.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Connekt_project.settings')

application = ProtocolTypeRouter({
'http': get_asgi_application(),
'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
        ),
    )
})
# application = get_asgi_application()
