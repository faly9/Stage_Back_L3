from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Freelance
from .serializers import FreelanceSerializer

class FreelanceViewSet(viewsets.ModelViewSet):
    serializer_class = FreelanceSerializer
    permission_classes = [permissions.IsAuthenticated]

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

    def perform_destroy(self, instance):
        # Vérification que l'utilisateur supprime son propre profil
        if instance.user != self.request.user:
            raise PermissionDenied("Vous n’êtes pas autorisé à supprimer ce profil.")
        instance.delete()

# Create your views here.
