from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # entreprise ou freelance

    if not email or not password:
        return Response({"error": "Email et mot de passe requis"}, status=400)

    if not role:
        return Response({"error": "Le rôle est requis (entreprise ou freelance)"}, status=400)

    if role not in [User.ROLE_ENTREPRISE, User.ROLE_FREELANCE]:
        return Response({"error": "Rôle invalide"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email déjà utilisé"}, status=400)

    user = User.objects.create_user(email=email, role=role, password=password)
    return Response({
        "message": "Utilisateur créé avec succès",
        "email": user.email,
        "role": user.role
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)  # ✅ crée la session
        return Response({
            "message": "Connexion réussie",
            "email": user.email,
            "role": user.role
        })
    else:
        return Response({"error": "Email ou mot de passe incorrect"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        "email": user.email,
        "role" : user.role
    })

@api_view(["POST"])
def logout_view(request):
    logout(request)  # ✅ supprime la session
    return Response({"message": "Déconnexion réussie"})


@api_view(["GET"])
def check_auth(request):
    if request.user.is_authenticated:
        return Response({"authenticated": True}, status=status.HTTP_200_OK)
    return Response({"authenticated": False}, status=status.HTTP_401_UNAUTHORIZED)
