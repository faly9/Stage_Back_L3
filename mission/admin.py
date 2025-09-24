# admin.py
from django.contrib import admin
from .models import Mission

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("id_mission", "titre","description", "budget", "entreprise")
    search_fields = ("titre", "competence_requis")
    list_filter = ("entreprise",)

