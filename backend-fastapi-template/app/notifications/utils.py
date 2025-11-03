from .manager import manager
from .schemas import Notification

async def send_notification(notification: Notification):
    message = f"{notification.title}: {notification.message}"
    await manager.broadcast(message)
