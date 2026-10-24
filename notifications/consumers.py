import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user:
            await self.close()
            return

        if not user.is_authenticated:
            await self.close()
            return

        self.group_name = f"notification_group_{user.pk}"
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )

        await self.accept()
        await self.send(
            text_data=json.dumps({
                "type": "connection_established",
                "message": "Connected to notification server",
            })
        )

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name, 
                self.channel_name,
            )

    async def notification_message(self, event):
        await self.send(
            text_data=json.dumps(event["notification"])
        )
