from django.db import models
from django.utils import timezone


class Candidature(models.Model):
    STATUS_CHOICES = [
        ("en_attente", "En attente"),        # quand le freelance postule
        ("recommandee", "Recommandée"),      # IA propose ce profil
        ("en_entretien", "En entretien"),    # entretien planifié ou en cours
    ]

    id_candidature = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="en_attente")

    # Relations
    mission = models.ForeignKey("mission.Mission", on_delete=models.CASCADE, related_name="candidatures")
    freelance = models.ForeignKey("freelance.Freelance", on_delete=models.CASCADE, related_name="candidatures")

    # Infos entretien
    date_entretien = models.DateTimeField(null=True, blank=True)  # date/heure prévue
    commentaire_entretien = models.TextField(null=True, blank=True)  # notes de l’entretien
    timezone = models.CharField(default="UTC",max_length=50) 

    # Score IA
    score = models.FloatField(default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["mission", "freelance"], name="unique_candidature")
        ]

    def __str__(self):
        return f"Candidature {self.id_candidature} ({self.get_status_display()})"
