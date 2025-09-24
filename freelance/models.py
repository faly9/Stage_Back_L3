from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Freelance(models.Model):
    id_freelance = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="freelance")
 
    nom = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    competence = models.TextField(null=False, blank=False)
    experience = models.TextField(null=False, blank=False)
    formation = models.TextField(null=False, blank=False)
    certificat = models.TextField(null=True, blank=True)

    tarif = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    photo = models.ImageField(upload_to="freelance_photos/", null=True, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.competence}"

# Create your models here.
