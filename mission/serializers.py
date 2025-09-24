from rest_framework import serializers
from .models import Mission

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id_mission', 'titre', 'description', 'competence_requis', 'budget', 'entreprise']
        read_only_fields = ['id_mission', 'entreprise']