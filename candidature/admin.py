from django.contrib import admin
from .models import Candidature


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ("id_candidature", "mission_titre", "freelance_nom", "status", "date", "score")
    list_filter = ("status", "date")
    search_fields = ("mission__titre", "freelance__nom")
    ordering = ("-date",)

    fieldsets = (
        ("Infos générales", {
            "fields": ("mission", "freelance", "status", "score")
        }),
        ("Entretien", {
            "fields": ("date_entretien", "commentaire_entretien"),
            "classes": ("collapse",),
        }),
        ("Métadonnées", {
            "fields": ("date",),
        }),
    )

    # Méthodes pour afficher les ForeignKey
    def mission_titre(self, obj):
        return obj.mission.titre
    mission_titre.short_description = "Mission"

    def freelance_nom(self, obj):
        return obj.freelance.nom
    freelance_nom.short_description = "Freelance"
