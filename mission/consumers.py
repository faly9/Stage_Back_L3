# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class MissionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "missions"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("✅ Connexion WebSocket pour les missions établie.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("❌ Connexion WebSocket fermée.")

    async def receive(self, text_data):
        """
        Permet de répondre aux messages manuels envoyés par le client (ex: refresh des missions).
        """
        data = json.loads(text_data)
        action = data.get("action")

        if action == "get_missions":
            from mission.models import Mission   # éviter import global
            missions = await sync_to_async(list)(Mission.objects.all().values())
            await self.send(text_data=json.dumps({
                "action": "list",
                "missions": missions
            }))

    # 🔹 Handlers pour écouter les events du group_send
    async def mission_created(self, event):
        await self.send(text_data=json.dumps({
            "action": "created",
            "mission": event["mission"]
        }))

    async def mission_updated(self, event):
        await self.send(text_data=json.dumps({
            "action": "updated",
            "mission": event["mission"]
        }))

    async def mission_deleted(self, event):
        await self.send(text_data=json.dumps({
            "action": "deleted",
            "mission": event["mission"]
        }))
