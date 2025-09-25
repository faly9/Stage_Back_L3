from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Mission
from entreprise.models import Entreprise
from .serializers import MissionSerializer
from rest_framework import viewsets, permissions


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        entreprise = Entreprise.objects.filter(user=user).first()
        if entreprise:
            return Mission.objects.filter(entreprise=entreprise)
        else:
            print("freelance")
        # Freelance → voir toutes les missions
            return Mission.objects.all()

    @action(detail=False, methods=["get", "post"], url_path="me")
    def me(self, request):
        user = request.user
        entreprise = Entreprise.objects.filter(user=user).first()

        if not entreprise:
            raise PermissionDenied("Seules les entreprises peuvent gérer leurs missions.")

        #  # Si c’est un freelance → afficher toutes les missions disponibles
        # if hasattr(user, "role") and user.role == "Freelance":
        #     return Mission.objects.all()

        # GET → récupérer missions de l'entreprise
        if request.method == "GET":
            # print("USER" , request.user)
            missions = Mission.objects.filter(entreprise=entreprise)
            serializer = self.get_serializer(missions, many=True)
            return Response(serializer.data)

        # POST → créer une nouvelle mission
        if request.method == "POST":
            # print("USER" , request.user)
            # print("DATA" , request.data)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(entreprise=entreprise)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     # 🔹 Méthode PUT / PATCH pour mettre à jour une mission
    def update(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.entreprise.user != request.user:
            raise PermissionDenied("Vous ne pouvez modifier que vos missions.")
        return super().update(request, *args, **kwargs)

    # 🔹 Méthode DELETE pour supprimer une mission
    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.entreprise.user != request.user:
            raise PermissionDenied("Vous ne pouvez supprimer que vos missions.")
        return super().destroy(request, *args, **kwargs)
