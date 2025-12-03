import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.integration
@pytest.mark.django_db
def test_register_user_integration(settings):
    """
    Test d'intégration complet du flux d'inscription :
    - Appel réel de l'API
    - Création réelle de l'utilisateur
    - Email réellement envoyé (in-memory)
    - Token réellement généré
    """

    settings.FRONTEND_URL = "http://localhost:5173"

    client = APIClient()

    payload = {
        "email": "test@gmail.com",
        "password": "StrongPassword123",
        "role": User.ROLE_FREELANCE,
    }

    # 1) Appel réel de l’API
    response = client.post(reverse("register"), payload, format="json")

    assert response.status_code == 201

    data = response.data

    # 2) Vérifications réponse
    assert data["email"] == payload["email"]
    assert data["role"] == payload["role"]
    assert "uid" in data
    assert "token" in data

    # 3) Vérifier création en BD
    user = User.objects.get(email="test@gmail.com")
    assert user.role == User.ROLE_FREELANCE
    assert user.is_active is False

    # 4) Vérifier email envoyé
    assert len(mail.outbox) == 1
    email_sent = mail.outbox[0]

    assert "Vérifie ton adresse e-mail" in email_sent.subject
    assert "test@gmail.com" in email_sent.to

    assert str(user.pk) in email_sent.body
    assert data["token"] in email_sent.body
