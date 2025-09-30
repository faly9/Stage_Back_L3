# candidature/routing.py
from django.urls import re_path
from .consumers import CandidatureConsumer , NotificationEntretienConsumer

websocket_urlpatterns = [
    # ⚠️ ici on définit un paramètre "entreprise_id" dans l'URL
    re_path(r'ws/candidatures/(?P<entreprise_id>\d+)/$', CandidatureConsumer.as_asgi()),
    re_path(r"ws/entretien/(?P<freelance_id>\d+)/$", NotificationEntretienConsumer.as_asgi()),
]
