from rest_framework import serializers
from .models import Freelance

class FreelanceSerializer(serializers.ModelSerializer):
    freelance_email = serializers.EmailField(source="user.email", read_only=True)
    photo = serializers.SerializerMethodField()  # champ personnalisé pour photo

    class Meta:
        model = Freelance
        fields = "__all__"
        read_only_fields = ["id_freelance", "user", "date_creation", "freelance_email"]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name  # renvoie seulement le chemin relatif /media/...
        return None
