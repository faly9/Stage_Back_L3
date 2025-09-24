from django.db import models
from entreprise.models import Entreprise  # adapte si ton app a un autre nom

class Mission(models.Model):
    id_mission = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    competence_requis = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name="mission")

    def __str__(self):
        return self.titre
