from rest_framework import serializers
from .models import Freelance

class FreelanceSerializer(serializers.ModelSerializer):
    freelance_email = serializers.EmailField(source="freelance.user.email", read_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Freelance
        fields = [
            "id_freelance",
            "user",
            "nom",
            "description",
            "competence",
            "experience",
            "formation",
            "certificat",
            "tarif",
            "photo",
            "date_creation",
            "freelance_email",
        ]
        read_only_fields = ["id_freelance", "user", "date_creation","freelance_email"]

    def to_representation(self, instance):
        """Retourner le chemin relatif pour la photo"""
        rep = super().to_representation(instance)
        if rep.get("photo"):
            rep["photo"] = instance.photo.name  # <-- chemin relatif
        return rep

