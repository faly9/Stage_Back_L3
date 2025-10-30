# entreprise/serializers.py
from rest_framework import serializers
from .models import Entreprise

class EntrepriseSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)  # <-- ajoute l'email ici
    profile_image = serializers.ImageField(use_url=True, required=False, allow_null=True)
    class Meta:
        model = Entreprise
        fields = ['id_entreprise', 'nom', 'secteur', 'user', 'profile_image', 'email']
        read_only_fields = ['id_entreprise', 'user', 'email']
