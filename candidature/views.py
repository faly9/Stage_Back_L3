# recrutement/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Candidature
from .serializers import CandidatureSerializer , UpdateCandidatureSerializer , notification
from entreprise.models import Entreprise
from freelance.models import Freelance

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def candidatures_mission(request):
    """
    Liste toutes les candidatures liées aux missions de l'entreprise connectée.
    """
    user = request.user
    entreprise = Entreprise.objects.filter(user=user).first()

    if not entreprise:
        return Response({"detail": "Vous devez être connecté en tant qu’entreprise."}, status=403)

    candidatures = Candidature.objects.filter(mission__entreprise=entreprise).order_by("-date")

    if not candidatures.exists():
        return Response({"detail": "Aucune candidature trouvée."}, status=200)

    serializer = CandidatureSerializer(candidatures, many=True)
    return Response(serializer.data)


@api_view(["GET","PATCH"])
@permission_classes([IsAuthenticated])
def update_candidature(request, pk):
    print("tonga etp")
    """
    Permet à une entreprise de modifier le statut ou la date d’entretien d’une candidature.
    """
    user = request.user
    entreprise = Entreprise.objects.filter(user=user).first()
    print(user)
    print(entreprise)

    if not entreprise:
        return Response({"detail": "Vous devez être connecté en tant qu’entreprise."}, status=403)

    try:
        candidature = Candidature.objects.get(pk=pk, mission__entreprise=entreprise)
    except Candidature.DoesNotExist:
        return Response({"detail": "Candidature introuvable ou non autorisée."}, status=404)

    serializer = UpdateCandidatureSerializer(candidature, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications_for_freelance(request):
    """
    Récupère toutes les candidatures liées au freelance connecté.
    """
    user = request.user
    freelance = Freelance.objects.filter(user=user).first()

    if not freelance:
        return Response({"detail": "Vous devez être connecté en tant que freelance."}, status=403)

    candidatures = Candidature.objects.filter(freelance=freelance).order_by("-date_entretien")
    serializer = notification(candidatures, many=True)

    return Response(serializer.data, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications_for_entreprise(request):
    """
    Récupère toutes les candidatures liées à l'entreprise connectée.
    """
    user = request.user
    entreprise = Entreprise.objects.filter(user=user).first()

    if not entreprise:
        return Response(
            {"detail": "Vous devez être connecté en tant qu'entreprise."}, status=403
        )

    candidatures = (
        Candidature.objects.filter(mission__entreprise=entreprise)
        .order_by("-date_entretien")
    )

    serializer = notification(candidatures, many=True)
    return Response(serializer.data, status=200)