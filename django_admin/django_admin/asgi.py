
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

import chats.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# application = get_asgi_application()

# django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(  
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),      
})