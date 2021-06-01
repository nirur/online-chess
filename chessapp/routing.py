from django.urls import path
from .consumers import PlayerConsumer, JsonWebsocketConsumer

websocket_urlpatterns = [
                         path('wss/<int:game_id>', JsonWebsocketConsumer.as_asgi()),
                        ]
