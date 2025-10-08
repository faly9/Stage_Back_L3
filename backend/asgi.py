import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ⚠️ 1. Définir le settings module AVANT tout import Django dépendant des modèles
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# ⚠️ 2. Créer l'application ASGI Django
django_asgi_app = get_asgi_application()

# ⚠️ 3. Importer les routing après l'initialisation de Django
import mission.routing
import candidature.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mission.routing.websocket_urlpatterns + candidature.routing.websocket_urlpatterns 
        )
    ),
})
