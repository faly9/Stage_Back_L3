from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Freelance
from .serializers import FreelanceSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class FreelanceViewSet(viewsets.ModelViewSet):
    serializer_class = FreelanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Chaque utilisateur ne peut voir que SON freelance
        return Freelance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Empêcher qu'un utilisateur crée plusieurs freelances
        if hasattr(self.request.user, "freelance"):
            raise PermissionDenied("Vous avez déjà un profil freelance.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Vérification que l'utilisateur modifie son propre profil
        freelance = self.get_object()
        if freelance.user != self.request.user:
            raise PermissionDenied("Vous n’êtes pas autorisé à modifier ce profil.")
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # 🔹 partial=True
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # Vérification que l'utilisateur supprime son propre profil
        if instance.user != self.request.user:
            raise PermissionDenied("Vous n’êtes pas autorisé à supprimer ce profil.")
        instance.delete()

# Create your views here.
