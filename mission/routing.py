from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/missions/$", consumers.MissionConsumer.as_asgi()),
]
