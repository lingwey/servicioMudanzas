from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/subasta/<int:subasta_id>/", consumers.SubastaConsumer.as_asgi()),
]
