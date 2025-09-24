from django.db import models
from django.conf import settings

class Entreprise(models.Model):
    id_entreprise = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    secteur = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entreprises"
    )
    profile_image = models.ImageField(
        upload_to='entreprises/profiles/',  # dossier dans MEDIA_ROOT
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom

