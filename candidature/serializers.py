# recrutement/serializers.py
from rest_framework import serializers
from .models import Candidature

class CandidatureSerializer(serializers.ModelSerializer):
    mission_titre = serializers.CharField(source="mission.titre", read_only=True)
    freelance_nom = serializers.CharField(source="freelance.nom", read_only=True)
    date = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)
    freelance_email = serializers.EmailField(source="freelance.user.email", read_only=True)
    # Récupérer l'ID de l'entreprise liée à la mission
    entreprise_id = serializers.IntegerField(source="mission.entreprise.id_entreprise", read_only=True)
    freelance_description = serializers.CharField(source="freelance.description", read_only=True)
    freelance_competence = serializers.CharField(source="freelance.competence", read_only=True)
    freelance_experience = serializers.CharField(source="freelance.experience", read_only=True)
    freelance_formation = serializers.CharField(source="freelance.formation", read_only=True)
    freelance_certificat = serializers.CharField(source="freelance.certificat", read_only=True)
    freelance_tarif = serializers.CharField(source="freelance.tarif", read_only=True)
    freelance_photo = serializers.CharField(source="freelance.photo", read_only=True)

    class Meta:
        model = Candidature
        fields = [
            "id_candidature",
            "date",
            "status",
            "mission",
            "freelance",
            "mission_titre",
            "freelance_nom",
            "entreprise_id",
            "freelance_email",
            "freelance_description",
            "freelance_competence",
            "freelance_experience",
            "freelance_formation",
            "freelance_certificat",
            "freelance_tarif",
            "freelance_photo",
            "date_entretien",
            "commentaire_entretien",
            "score",
        ]
        # Ces champs sont fixes → jamais modifiables
        read_only_fields = [
            "id_candidature", 
            "mission", 
            "mission_titre", 
            "freelance", 
            "freelance_nom", 
            "freelance_email",
            "freelance_description",
            "freelance_competence",
            "freelance_experience",
            "freelance_formation",
            "freelance_certificat",
            "freelance_tarif",
            "freelance_photo",
            "date"  # générée automatiquement
        ]


class UpdateCandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = ["id_candidature","status", "date_entretien", "commentaire_entretien", "score"]
        read_only_fields=["id_candidature"]

class notification(serializers.ModelSerializer):
    mission_titre = serializers.CharField(source="mission.titre", read_only=True)
    freelance_nom = serializers.CharField(source="freelance.nom", read_only=True)
    entreprise_nom = serializers.CharField(source="mission.entreprise.nom" , read_only=True)
    entreprise_photo = serializers.CharField(source="mission.entreprise.profile_image" , read_only=True)

    class Meta:
        model = Candidature
        fields = ["id_candidature","entreprise_photo","entreprise_nom","mission_titre","freelance_nom","status", "date_entretien", "commentaire_entretien"]
