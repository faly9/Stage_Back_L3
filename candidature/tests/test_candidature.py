# recrutement/tests/test_candidature_views.py
from django.test import override_settings
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from candidature.models import Candidature
import pytest
from mission.models import Mission
from entreprise.models import Entreprise
from freelance.models import Freelance
from datetime import datetime, timedelta

User = get_user_model()

@pytest.mark.unit
@override_settings(
    CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
)
class CandidatureViewsTest(APITestCase):

    def setUp(self):
        # Création utilisateurs
        self.user_entreprise = User.objects.create_user(
            email="entreprise@gmail.com", password="pass123", role=User.ROLE_ENTREPRISE
        )
        self.user_freelance = User.objects.create_user(
            email="freelance@gmail.com", password="pass123", role=User.ROLE_FREELANCE
        )

        # Entreprise et Freelance
        self.entreprise = Entreprise.objects.create(
            user=self.user_entreprise, nom="Entreprise Test", secteur="IT"
        )
        self.freelance = Freelance.objects.create(
            user=self.user_freelance, nom="Freelance Test" , tarif="75.00"
        )

        # Mission
        self.mission = Mission.objects.create(
            titre="Mission Test",
            description="Description",
            competence_requis="Python",
            budget=1000,
            entreprise=self.entreprise
        )

        # Candidature
        self.candidature = Candidature.objects.create(
            mission=self.mission,
            freelance=self.freelance,
            status="en_attente",
            date_entretien=datetime.now() + timedelta(days=1),
            timezone="UTC"
        )

    # -------------------------------
    # Liste candidatures pour entreprise
    # -------------------------------
    def test_candidatures_mission_success(self):
        self.client.login(email="entreprise@gmail.com", password="pass123")
        url = reverse("mes_candidatures")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id_candidature"], self.candidature.id_candidature)

    def test_candidatures_mission_forbidden_for_freelance(self):
        self.client.login(email="freelance@gmail.com", password="pass123")
        url = reverse("mes_candidatures")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # -------------------------------
    # Mise à jour candidature
    # -------------------------------
    def test_update_candidature_status(self):
        self.client.login(email="entreprise@gmail.com", password="pass123")
        url = reverse("candidatureupdate", kwargs={"pk": self.candidature.id_candidature})
        data = {"status": "en_entretien"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.candidature.refresh_from_db()
        self.assertEqual(self.candidature.status, "en_entretien")

    def test_update_candidature_not_allowed(self):
        self.client.login(email="freelance@gmail.com", password="pass123")
        url = reverse("candidatureupdate", kwargs={"pk": self.candidature.id_candidature})
        data = {"status": "en_entretien"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    # -------------------------------
    # Notifications pour freelance
    # -------------------------------
    def test_get_notifications_for_freelance_success(self):
        self.client.login(email="freelance@gmail.com", password="pass123")
        url = reverse("notifications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id_candidature"], self.candidature.id_candidature)
        self.assertEqual(response.json()[0]["timezone"], "UTC")

    # -------------------------------
    # Notifications pour entreprise
    # -------------------------------
    def test_get_notifications_for_entreprise_success(self):
        self.client.login(email="entreprise@gmail.com", password="pass123")
        url = reverse("notifications-entreprise")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id_candidature"], self.candidature.id_candidature)


# 5️⃣ Résumé du fonctionnement réel

# Authentification obligatoire → seules les entreprises ou freelances
#  connectés peuvent accéder aux endpoints pertinents.

# Liste de candidatures → filtrée selon le rôle de l’utilisateur.

# Mise à jour des candidatures → réservée à l’entreprise propriétaire
#  de la mission.

# Notifications en temps réel → permettent à l’entreprise et au
#  freelance de suivre l’évolution des candidatures via WebSocket.

# Les tests valident à la fois la logique métier (droits d’accès,
#  filtres) et la cohérence des données renvoyées.