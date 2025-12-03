from django.urls import reverse
import pytest
from rest_framework.test import APITestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()
@pytest.mark.unit

class AuthLoginTest(APITestCase):

    @patch("authentification.views.login")
    @patch("authentification.views.authenticate")
    def test_login_user_success(self, mock_authenticate, mock_login):

        print("\n--- DÉBUT TEST : test_login_user_success ---")

        # 👉 utiliser un VRAI USER Django
        user = User.objects.create(
            email="test@example.com",
            role="Freelance",
            password=make_password("123456")
        )
        print("[INFO] Vrai user créé ✔")

        # 👉 authenticate renvoie ce vrai user
        mock_authenticate.return_value = user

        url = reverse("login")
        data = {
            "email": "test@example.com",
            "password": "123456"
        }

        print("[REQUEST] POST /login")
        response = self.client.post(url, data, format="json")

        print("[CHECK] Status code :", response.status_code)
        self.assertEqual(response.status_code, 200)

        # 👉 login doit être appelé
        mock_login.assert_called_once()
        print("[SUCCESS] login() called ✔")

        # 👉 vérifier que login reçoit le bon user
        _, call_user = mock_login.call_args[0]
        self.assertEqual(call_user, user)
        print("[SUCCESS] login() a reçu le bon user ✔")

        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["role"], "Freelance")

        print("[SUCCESS] Réponse correcte ✔")
        print("--- FIN TEST ---\n")


# Le test test_login_user_success illustre le fonctionnement 
# de la vue de connexion de notre application. Lorsqu’un utilisateur
#  envoie ses identifiants (email et password) à l’API, le backend 
#  utilise la fonction authenticate() pour vérifier que ces informations
# correspondent à un utilisateur enregistré dans la base de données.
#  Si l’authentification réussit, la fonction login() de Django est 
#  appelée afin de créer une session pour cet utilisateur et de le 
#  considérer comme connecté. Ensuite, la vue renvoie une réponse JSON 
#  contenant les informations essentielles de l’utilisateur, comme son
#   adresse email et son rôle, que le frontend pourra utiliser pour 
#   adapter l’interface.

# Le test simule ce processus en créant un utilisateur réel dans la
#  base de données de test et en contrôlant les appels aux fonctions 
#  authenticate() et login() grâce au mocking. Cela permet de vérifier
#   que la logique de la vue fonctionne correctement : l’utilisateur 
#   est authentifié, la session est créée et la réponse contient les 
#   bonnes informations. Ainsi, même sans exécuter l’intégralité du 
#   système d’authentification Django ou gérer les sessions réelles,
#    le test garantit que la vue login remplit correctement son rôle.