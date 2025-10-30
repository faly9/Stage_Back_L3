# entreprise/serializers.py
from rest_framework import serializers
from .models import Entreprise

class EntrepriseSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)  # <-- ajoute l'email ici
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = Entreprise
        fields = ['id_entreprise', 'nom', 'secteur', 'user', 'profile_image', 'email']
        read_only_fields = ['id_entreprise', 'user', 'email']
        
    def get_profile_image(self, obj):
        if obj.profile_image:
            # renvoie uniquement le chemin relatif
            return obj.profile_image.url.replace(obj.profile_image.storage.base_url, '')  
        return None