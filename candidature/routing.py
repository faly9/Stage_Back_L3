# candidature/routing.py
from django.urls import re_path
from .consumers import CandidatureConsumer

websocket_urlpatterns = [
    # ⚠️ ici on définit un paramètre "entreprise_id" dans l'URL
    re_path(r'ws/candidatures/(?P<entreprise_id>\d+)/$', CandidatureConsumer.as_asgi()),
]
