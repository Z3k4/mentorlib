import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from mentorlib.apps.users.models import Notification


@database_sync_to_async
def read_notification(id):
    notification = Notification.objects.get(id=id)
    notification.readed = True
    notification.save()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"]:
            self.user_channel = f"user_{self.scope['user'].id}"

            await self.channel_layer.group_add(self.user_channel, self.channel_name)

            await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        notification_id = data["readed"]
        await read_notification(notification_id)

    async def disconnect(self, close_code):
        pass

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["content"]))
