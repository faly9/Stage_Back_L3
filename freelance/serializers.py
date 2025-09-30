from rest_framework import serializers
from .models import Freelance

class FreelanceSerializer(serializers.ModelSerializer):
    freelance_email = serializers.EmailField(source="freelance.user.email", read_only=True)
    class Meta:
        model = Freelance
        fields = "__all__"
        read_only_fields = ["id_freelance", "user", "date_creation","freelance_email"]
