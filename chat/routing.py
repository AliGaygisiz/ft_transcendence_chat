from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # write a path to get the chat consumer with username as a parameter
    # e.g. ws/socket-server/username/
    re_path(r"ws/global-chat/", consumers.ChatConsumer.as_asgi()),
]
