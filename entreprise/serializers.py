# entreprise/serializers.py
from rest_framework import serializers
from .models import Entreprise

class EntrepriseSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Entreprise
        fields = ['id_entreprise', 'nom', 'secteur', 'user', 'profile_image', 'email']
        read_only_fields = ['id_entreprise', 'user', 'email']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # 🔹 garder seulement le chemin relatif pour profile_image
        if rep.get("profile_image"):
            rep["profile_image"] = instance.profile_image.name  # chemin relatif
        return rep
