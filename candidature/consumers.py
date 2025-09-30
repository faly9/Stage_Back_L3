import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError 
from .models import Candidature
from mission.models import Mission
from freelance.models import Freelance


class CandidatureConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.entreprise_id = self.scope['url_route']['kwargs']['entreprise_id']
        self.group_name = f"entreprise_{self.entreprise_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ WebSocket connecté pour entreprise {self.entreprise_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # --- Nouvelle fonction synchrone pour la logique ORM ---
    @sync_to_async
    def handle_candidature_sync(self, mission_id, freelance_id, entreprise_id):
        """
        Effectue toutes les opérations synchrones (ORM) :
        - Récupération des objets.
        - Vérification de la propriété de la mission.
        - Création/Récupération de la candidature (get_or_create).
        - Sérialisation des données pour la réponse.
        """
        
        try:
            # 1. Récupération des objets
            mission = Mission.objects.select_related("entreprise").get(id_mission=mission_id)
            freelance = Freelance.objects.select_related("user").get(id_freelance=freelance_id)
            
            # 2. Vérification de la propriété
            if str(mission.entreprise.id_entreprise) != entreprise_id:
                return {"error": "Sécurité: Mission non valide pour cette entreprise."}

            # 3. Création ou Récupération de la Candidature
            candidature, created = Candidature.objects.get_or_create(
                mission=mission,
                freelance=freelance,
                defaults={"status": "en_attente"}
            )
            
            # 4. Sérialisation des données (y compris l'accès à freelance.user.email)
            response = {
                "id_candidature": candidature.id_candidature,
                "date": candidature.date.strftime("%Y-%m-%d"),
                "status": candidature.status,
                "mission_titre": mission.titre,
                "freelance_nom": freelance.nom,
                "freelance_description": freelance.description,
                "freelance_competence": freelance.competence,
                "freelance_experience": freelance.experience,
                "freelance_formation": freelance.formation,
                "freelance_certificat": freelance.certificat,
                "freelance_tarif": str(freelance.tarif),
                # L'accès à `freelance.user.email` est sûr car nous sommes dans un thread synchrone.
                "freelance_email": freelance.user.email if hasattr(freelance, 'user') else "Email non disponible",
                "freelance_photo": str(freelance.photo) if freelance.photo else None,
                "created": created 
            }
            
            return {"success": response, "created": created}
            
        except ObjectDoesNotExist:
            return {"error": "Mission ou Freelance non trouvé."}
        except IntegrityError:
            return {"error": "Erreur d'intégrité de la base de données (doublon)." }
        except Exception as e:
            return {"error": f"Erreur interne: {str(e)}"}


    async def receive(self, text_data):
        data = json.loads(text_data)
        mission_id = data.get("mission_id")
        freelance_id = data.get("freelance_id")
        
        # --- Appel asynchrone à la fonction synchrone ---
        result = await self.handle_candidature_sync(
            mission_id, 
            freelance_id, 
            self.entreprise_id
        )

        if "error" in result:
            print(f"🚫 Erreur: {result['error']}")
            await self.send(text_data=json.dumps({"error": result['error']}))
            return

        # Le résultat est un succès, on diffuse.
        response = result["success"]
        created = result["created"]

        if not created:
             print(f"⚠️ Candidature existante (Mission: {mission_id}, Freelance: {freelance_id}).")
        else:
             print(f"✅ Nouvelle candidature créée (Mission: {mission_id}, Freelance: {freelance_id}).")


        # Diffuser la candidature uniquement au groupe de l'entreprise
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "new_candidature", "message": response}
        )

    # Méthode appelée automatiquement pour chaque message du groupe
    async def new_candidature(self, event):
        await self.send(text_data=json.dumps(event["message"]))




class NotificationEntretienConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.freelance_id = self.scope['url_route']['kwargs']['freelance_id']
        self.group_name = f"freelance_{self.freelance_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"✅ WS connecté pour Freelance {self.freelance_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def new_entretien(self, event):
        """
        Reçoit les notifications du signal et les envoie au frontend.
        """
        await self.send(text_data=json.dumps(event["message"]))
