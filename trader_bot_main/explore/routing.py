from django.urls import path
from .consumers import CryptoDataConsumer

websocket_urlpatterns = [
    path('ws/crypto-data/', CryptoDataConsumer.as_asgi()),
]
