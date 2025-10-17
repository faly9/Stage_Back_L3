from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings  # pour utiliser settings.DEFAULT_FROM_EMAIL



@api_view(['POST'])
def register_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # entreprise ou freelance
    
    # --- 1️⃣ Vérifications de base ---
    if not email or not password:
        return Response({"error": "Email et mot de passe requis"}, status=400)

    if not role:
        return Response({"error": "Le rôle est requis (entreprise ou freelance)"}, status=400)

    if role not in [User.ROLE_ENTREPRISE, User.ROLE_FREELANCE]:
        return Response({"error": "Rôle invalide"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email déjà utilisé"}, status=400)

    # --- 2️⃣ Créer l’utilisateur inactif ---
    user = User.objects.create_user(email=email, role=role, password=password, is_active=False)
    user.save()

    # --- 3️⃣ Générer le lien de vérification ---
    token = default_token_generator.make_token(user)
    verification_link = f"http://localhost:5173/verify/{user.pk}/{token}"  # lien côté React
    print(verification_link)

    # --- 4️⃣ Envoyer le mail de vérification ---
    subject = "Vérifie ton adresse e-mail"
    message = f"""
    Bonjour,
    
    Merci pour ton inscription sur notre plateforme.
    Clique sur le lien ci-dessous pour vérifier ton adresse e-mail :
    
    {verification_link}
    
    Si tu n'es pas à l'origine de cette inscription, ignore simplement ce message.
    
    -- L'équipe Support
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    # --- 5️⃣ Retourner la réponse ---
    return Response({
        "message": "Utilisateur créé avec succès. Un e-mail de vérification a été envoyé.",
        "email": user.email,
        "role": user.role,
        "uid": user.pk,       # ✅ ajouter l'uid
        "token": token        # ✅ ajouter le token
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    # 🔹 Vérifie d'abord si l'utilisateur existe
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Email ou mot de passe incorrect"}, status=400)

    # 🔹 Vérifie si le compte est actif (confirmé)
    if not user.is_active:
        return Response(
            {"error": "Votre compte n’a pas encore été confirmé. Veuillez vérifier votre e-mail."},
            status=403
        )

    # 🔹 Authentifie ensuite si le compte est actif
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
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


@api_view(['GET'])
def verify_email(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return Response({"success": False, "message": "Utilisateur introuvable"}, status=404)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Retourne l’information à React pour qu’il redirige
        return Response({"success": True, "message": "Compte activé"})
    else:
        return Response({"success": False, "message": "Token invalide"}, status=400)
