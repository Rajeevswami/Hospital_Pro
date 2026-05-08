"""WebSocket consumer and routing for real-time notifications."""
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.urls import re_path


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        if not self.user or self.user.is_anonymous:
            await self.close()
            return
        self.group_name = f'notifications_{self.user.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        action = content.get('action')
        if action == 'mark_read':
            notification_id = content.get('id')
            await self.mark_as_read(notification_id)
            await self.send_json({'action': 'marked_read', 'id': notification_id})

    async def send_notification(self, event):
        await self.send_json(event['data'])

    @database_sync_to_async
    def mark_as_read(self, notification_id):
        from .models import Notification
        from django.utils import timezone
        Notification.objects.filter(id=notification_id, user=self.user).update(
            is_read=True, read_at=timezone.now()
        )


# WebSocket URL routing
websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
