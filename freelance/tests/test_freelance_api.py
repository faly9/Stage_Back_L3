from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
import pytest
from rest_framework.reverse import reverse
from freelance.models import Freelance

User = get_user_model()
@pytest.mark.unit

class FreelanceAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            role=User.ROLE_FREELANCE,
            password="password123",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("freelance-list")  # URL pour création/list

    def test_create_freelance(self):
        data = {
            "nom": "Jean Dupont",
            "description": "Développeur web",
            "competence": "Python, Django, React",
            "experience": "3 ans",
            "formation": "Master informatique",
            "certificat": "Certifié DRF",
            "tarif": "50.00",
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Freelance.objects.count(), 1)
        self.assertEqual(Freelance.objects.first().user, self.user)

    def test_list_freelance(self):
        Freelance.objects.create(
            user=self.user,
            nom="Jean Dupont",
            description="Développeur web",
            competence="Python, Django, React",
            experience="3 ans",
            formation="Master informatique",
            tarif="50.00"
        )
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["nom"], "Jean Dupont")


# Utilisateur connecté → l’API vérifie son rôle et son existence.

# POST /freelances/ → crée un profil freelance pour cet utilisateur.

# GET /freelances/ → liste les profils existants.

# Liens entre tables → chaque profil Freelance est associé à un User,
#  ce qui permet de sécuriser les données.

# Les tests garantissent que la création, 
# la liaison utilisateur et la récupération fonctionnent correctement.
