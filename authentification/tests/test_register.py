from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.contrib.auth.hashers import make_password
User = get_user_model()


@pytest.mark.unit
class RegisterUserTest(APITestCase):

    @patch("authentification.views.send_mail")   # 👉 ON MOCK ICI
    def test_register_user_success(self, mock_send_mail):
        url = reverse("register")  # Ton endpoint
        data = {
            "email": "test@example.com",
            "password": "123456",
            "role": User.ROLE_FREELANCE,
        }

        response = self.client.post(url, data, format="json")

        # ---- 1️⃣ Vérifier le code HTTP ----
        self.assertEqual(response.status_code, 201)

        # ---- 2️⃣ Vérifier que l'utilisateur est créé ----
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

        # ---- 3️⃣ Vérifier que send_mail a été appelé ----
        mock_send_mail.assert_called_once()

        # ---- 4️⃣ Vérifier que la réponse contient les champs ----
        self.assertIn("token", response.data)
        print(response.data)
        self.assertIn("uid", response.data)

# Le test test_register_user_success illustre le fonctionnement 
# de la vue d’inscription de notre application. Lorsqu’un nouvel
#  utilisateur soumet son email, son mot de passe et son rôle à l’API, 
# la vue crée un utilisateur dans la base de données et génère un token 
# ainsi qu’un identifiant unique (uid) pour cet utilisateur. Ensuite,
#  un email de confirmation est envoyé pour valider l’adresse email 
#  fournie.

# Dans le test, l’envoi réel de l’email est simulé grâce 
# au mocking de la fonction send_mail. Cela permet de vérifier
#  que la vue appelle bien cette fonction sans avoir besoin d’envoyer 
#  un vrai email. Le test vérifie également que l’utilisateur est bien
#   créé dans la base de données, que le code HTTP de la réponse est 
#   correct (201 Created), et que les champs token et uid sont présents
#    dans la réponse JSON.

# Ainsi, même sans exécuter l’envoi réel d’emails, le test
#  garantit que la vue d’inscription fonctionne correctement : 
#  l’utilisateur est enregistré, un token est généré et la logique 
#  d’email de confirmation est déclenchée.