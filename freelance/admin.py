from django.contrib import admin
from .models import Freelance

@admin.register(Freelance)
class FreelanceAdmin(admin.ModelAdmin):
    list_display = ("id_freelance", "nom", "description",  "tarif", "competence", "experience", "formation" , "certificat", "user" , "photo")
    search_fields = ("nom", "competence", "experience", "formation")
