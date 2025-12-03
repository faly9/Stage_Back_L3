from django.urls import reverse
import pytest
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()
@pytest.mark.integration

class LoginIntegrationTest(APITestCase):

    def setUp(self):
        # Création d'un vrai user dans la base de données de test
        self.user = User.objects.create(
            email="test@example.com",
            role="Freelance",
            password=make_password("123456"),  # hashing réel
            is_active=True
        )
        self.url = reverse("login")   # doit pointer vers login_user

    def test_login_success_integration(self):
        """ Vérifie que le login fonctionne réellement sans mocking """

        data = {
            "email": "test@example.com",
            "password": "123456"
        }

        response = self.client.post(self.url, data, format="json")

        # Vérifications
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["role"], "Freelance")
        self.assertIn("message", response.data)

    def test_login_wrong_password(self):
        """ Mot de passe incorrect -> 400 """

        data = {
            "email": "test@example.com",
            "password": "wrong"
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Email ou mot de passe incorrect")

    def test_login_user_not_exist(self):
        """ Email inexistant -> 400 """

        data = {
            "email": "notfound@example.com",
            "password": "123456"
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Email ou mot de passe incorrect")

    def test_login_user_not_active(self):
        """ Compte non confirmé -> 403 """

        # Crée un user inactif
        inactive_user = User.objects.create(
            email="inactive@example.com",
            role="Freelance",
            password=make_password("123456"),
            is_active=False
        )

        data = {
            "email": "inactive@example.com",
            "password": "123456"
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["error"],
            "Votre compte n’a pas encore été confirmé. Veuillez vérifier votre e-mail."
        )
