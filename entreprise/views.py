from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Entreprise
from .serializers import EntrepriseSerializer
from rest_framework.decorators import action
from rest_framework import status
from django.http import JsonResponse

class EntrepriseViewSet(viewsets.ModelViewSet):
    serializer_class = EntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entreprise.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get", "post"], url_path="me")
    def me(self, request):
        entreprise = Entreprise.objects.filter(user=request.user).first()

        # Récupération
        if request.method == "GET":
            if not entreprise:
                return Response({"detail": "Profil inexistant"}, status=404)
            serializer = self.get_serializer(entreprise)
            return Response(serializer.data)

        # Création si inexistant, sinon update
        if request.method == "POST":
            if entreprise:
                serializer = self.get_serializer(
                    entreprise, data=request.data, partial=True
                )
            else:
                serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_my_entreprise(request):
    entreprise = Entreprise.objects.get(user=request.user)
    print(entreprise.id_entreprise)
    return JsonResponse({"entreprise_id": entreprise.id_entreprise})