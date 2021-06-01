from django.urls import path
from .consumers import PlayerConsumer

websocket_urlpatterns = [
                         path('wss/<int:game_id>', PlayerConsumer.as_asgi()),
                        ]
