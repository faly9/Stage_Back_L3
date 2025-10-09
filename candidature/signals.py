# recrutement/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Candidature
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Candidature)
def candidature_updated(sender, instance, created, **kwargs):
    """
    Envoie une notification WebSocket uniquement lorsqu'une candidature est mise à jour,
    pas lors de sa création.
    """
    # Si la candidature vient d'être créée, on ne fait rien
    if created:
        return

    # On peut aussi vérifier que certains champs spécifiques ont changé, si nécessaire
    # Par exemple: status ou date_entretien
    # Si tu utilises serializer.save(update_fields=[...]) dans ta vue,
    # tu peux récupérer kwargs['update_fields'] et filtrer

    channel_layer = get_channel_layer()
    freelance_id = instance.freelance.id_freelance
    entreprise_id = instance.mission.entreprise.id_entreprise  # ID de l'entreprise


    message = {
        "id_candidature": instance.id_candidature,
        "status": instance.status,
        "date_entretien": str(instance.date_entretien) if instance.date_entretien else None,
        "commentaire_entretien": instance.commentaire_entretien,
        "timezone" : instance.timezone,
        "mission_titre": instance.mission.titre,
        "entreprise_nom": instance.mission.entreprise.nom,
        "entreprise_photo": instance.mission.entreprise.profile_image.url if instance.mission.entreprise.profile_image else None,
        "freelance_nom": instance.freelance.nom,
    }

    async_to_sync(channel_layer.group_send)(
        f"freelance_{freelance_id}",
        {
            "type": "new_entretien",
            "message": message
        }
    )

     # ✅ Envoi à l'entreprise pour visualisation
    async_to_sync(channel_layer.group_send)(
        f"entreprise_{entreprise_id}",
        {
            "type": "new_entretien",
            "message": message
        }
    )

