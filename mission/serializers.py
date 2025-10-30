from rest_framework import serializers
from .models import Mission

class MissionSerializer(serializers.ModelSerializer):
    entreprise_nom = serializers.CharField(source="entreprise.nom", read_only=True)
    entreprise_secteur = serializers.CharField(source="entreprise.secteur", read_only=True)
    entreprise_photo = serializers.SerializerMethodField()  # chemin relatif seulement

    class Meta:
        model = Mission
        fields = [
            "id_mission",
            "titre",
            "description",
            "competence_requis",
            "budget",
            "entreprise",
            "entreprise_nom",
            "entreprise_secteur",
            "entreprise_photo",
        ]
        read_only_fields = ['id_mission', 'entreprise']

    def get_entreprise_photo(self, obj):
        if obj.entreprise.profile_image:
            # renvoie uniquement le chemin relatif
            return obj.entreprise.profile_image.name  
        return None
