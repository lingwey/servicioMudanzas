import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import creacionSubastas.routing  # app con WebSocket consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mudanzas.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # sigue respondiendo a peticiones HTTP normales
    "websocket": AuthMiddlewareStack(
        URLRouter(
            creacionSubastas.routing.websocket_urlpatterns 
        )
    ),
})
