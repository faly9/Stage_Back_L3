# mission/tests/test_mission_api.py
from django.test import override_settings
from rest_framework.test import APITestCase
import pytest
from django.contrib.auth import get_user_model
from mission.models import Mission, Entreprise

User = get_user_model()
@pytest.mark.unit
@override_settings(
    CHANNEL_LAYERS={
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }
)
class MissionAPITest(APITestCase):

    def setUp(self):
        # Créer un utilisateur et une entreprise
        self.user = User.objects.create_user(
            email="user1@gmail.com", password="pass123" , role=User.ROLE_ENTREPRISE)
        self.other_user = User.objects.create_user(
            email="user2@gmail.com", password="pass123" , role=User.ROLE_ENTREPRISE)
        self.entreprise = Entreprise.objects.create(
            user=self.user,
            nom="Entreprise Test",
            secteur="Informatique",
        )
        self.client.login(email="user1@gmail.com", password="pass123")
        self.url_me = "/msn/missions/me/"  # adapte si nécessaire

    def test_me_post_create_mission(self):
        data = {
            "titre": "Mission Test",
            "description": "Description test",
            "competence_requis": "Python",
            "budget": 1000,
        }
        response = self.client.post(self.url_me, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Mission.objects.count(), 1)
        mission = Mission.objects.first()
        self.assertEqual(mission.titre, "Mission Test")
        self.assertEqual(mission.entreprise, self.entreprise)

    def test_me_get_list_missions(self):
        # Créer une mission
        Mission.objects.create(
            titre="Mission 1",
            description="Desc",
            competence_requis="Django",
            budget=500,
            entreprise=self.entreprise
        )
        response = self.client.get(self.url_me)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_mission_owner(self):
        mission = Mission.objects.create(
            titre="Mission 2",
            description="Desc",
            competence_requis="DRF",
            budget=800,
            entreprise=self.entreprise
        )
        data = {"titre": "Mission 2 modifiée"}
        response = self.client.patch(f"/msn/missions/{mission.id_mission}/", data, format="json")
        self.assertEqual(response.status_code, 200)
        mission.refresh_from_db()
        self.assertEqual(mission.titre, "Mission 2 modifiée")

    def test_update_mission_not_owner(self):
        mission = Mission.objects.create(
            titre="Mission 3",
            description="Desc",
            competence_requis="React",
            budget=300,
            entreprise=self.entreprise
        )
        self.client.login(email="user2@gmail.com", password="pass123")
        data = {"titre": "Mission 3 modifiée"}
        response = self.client.patch(f"/msn/missions/{mission.id_mission}/", data, format="json")
        self.assertEqual(response.status_code, 403)  # Not allowed

    def test_delete_mission_owner(self):
        mission = Mission.objects.create(
            titre="Mission 4",
            description="Desc",
            competence_requis="Vue",
            budget=200,
            entreprise=self.entreprise
        )
        response = self.client.delete(f"/msn/missions/{mission.id_mission}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Mission.objects.count(), 0)

# Résumé du fonctionnement réel

# Authentification obligatoire → seul un utilisateur connecté peut gérer ses missions.

# POST /me → création d’une mission liée à l’entreprise.

# GET /me → récupération de toutes les missions de l’entreprise.

# PATCH /<id> → modification sécurisée par l’utilisateur propriétaire.

# DELETE /<id> → suppression sécurisée par l’utilisateur propriétaire.

# Les tests valident que les permissions et la logique métier fonctionnent correctement.