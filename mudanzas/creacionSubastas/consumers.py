import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SubastaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.subasta_id = self.scope["url_route"]["kwargs"]["subasta_id"]
        self.room_group_name = f"subasta_{self.subasta_id}"

        # Unirse al grupo de la subasta
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # por ahora no procesamos nada del cliente, solo pasamos

    async def enviar_oferta(self, event):
        # Este método se llama cuando se emite una nueva oferta desde el backend
        await self.send(text_data=json.dumps({
            "tipo": "nueva_oferta",
            "html": event["html"]
        }))
