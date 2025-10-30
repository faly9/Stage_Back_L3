from rest_framework import serializers
from .models import Freelance

class FreelanceSerializer(serializers.ModelSerializer):
    freelance_email = serializers.EmailField(source="user.email", read_only=True)
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Freelance
        fields = "__all__"
        read_only_fields = ["id_freelance", "user", "date_creation", "freelance_email"]

    def get_photo(self, obj):
        if obj.photo:
            # renvoie uniquement le chemin relatif
            return obj.photo.url.replace(obj.photo.storage.base_url, '')  
        return None
