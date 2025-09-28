# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Mission

def _serialize_mission(instance):
    """
    Sérialiser les champs nécessaires pour le WebSocket.
    """
    entreprise = instance.entreprise
    return {
        "id_mission": instance.id_mission,
        "titre": instance.titre,
        "description": instance.description,
        "competence_requis": instance.competence_requis,
        "budget": float(instance.budget),
        "entreprise_nom": entreprise.nom if entreprise else None,
        "entreprise_secteur": entreprise.secteur if entreprise else None ,
        "entreprise_photo": entreprise.profile_image.url if entreprise and entreprise.profile_image else None, 
        }

@receiver(post_save, sender=Mission)
def notify_mission_save(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    action_type = "mission_created" if created else "mission_updated"

    async_to_sync(channel_layer.group_send)(
        "missions",
        {
            "type": action_type,  # doit matcher les handlers du consumer
            "mission": _serialize_mission(instance),
        },
    )

@receiver(post_delete, sender=Mission)
def notify_mission_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "missions",
        {
            "type": "mission_deleted",
            "mission": {"id_mission": instance.id_mission},  # envoie juste l’ID
        },
    )
