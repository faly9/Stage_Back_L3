from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
import pytest
from entreprise.models import Entreprise

User = get_user_model()
@pytest.mark.unit

class EntrepriseAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="entreprise@test.com",
            role=User.ROLE_ENTREPRISE,
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url_me = reverse("entreprise-me")  # /entreprises/me/
        self.url_id = reverse("id-entreprise")  # /entreprises/id/

    def test_me_get_no_entreprise(self):
        """GET /me retourne 404 si pas de profil"""
        response = self.client.get(self.url_me)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Profil inexistant")

    def test_me_post_create_entreprise(self):
        """POST /me crée un profil entreprise"""
        data = {
            "nom": "Ma Société",
            "secteur": "Informatique"
        }
        response = self.client.post(self.url_me, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Entreprise.objects.count(), 1)
        entreprise = Entreprise.objects.first()
        self.assertEqual(entreprise.user, self.user)
        self.assertEqual(entreprise.nom, "Ma Société")

    def test_me_post_update_entreprise(self):
        """POST /me met à jour le profil existant"""
        Entreprise.objects.create(user=self.user, nom="Old Name", secteur="Ancien Secteur")
        data = {"nom": "New Name"}
        response = self.client.post(self.url_me, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entreprise = Entreprise.objects.get(user=self.user)
        self.assertEqual(entreprise.nom, "New Name")

    def test_get_my_entreprise(self):
        """GET /id/ retourne l'id de l'entreprise"""
        entreprise = Entreprise.objects.create(user=self.user, nom="Test", secteur="IT")
        response = self.client.get(self.url_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"entreprise_id": entreprise.id_entreprise})

    def test_get_my_entreprise_not_exist(self):
        """GET /id/ retourne 404 si pas d'entreprise"""
        response = self.client.get(self.url_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Aucune entreprise associée à cet utilisateur."})


# Chaque vue utilise l’utilisateur connecté pour identifier
#  le profil entreprise.

# /me/ est polyvalente : elle crée ou met à jour un
#  profil selon qu’il existe ou non.

# /id/ sert à récupérer uniquement l’ID du profil.

# Les tests couvrent toutes les situations possibles : 
# profil inexistant, création, mise à jour, lecture avec
#  et sans profil.

# Cela montre que la logique côté serveur est robuste et
#  sécurisée : seules les actions autorisées par l’état actuel
#   de l’utilisateur sont exécutées.