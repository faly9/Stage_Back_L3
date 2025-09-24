from rest_framework import serializers
from .models import Freelance

class FreelanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelance
        fields = "__all__"
        read_only_fields = ["id_freelance", "user", "date_creation"]
