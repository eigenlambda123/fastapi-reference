from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from .manager import manager
from .schemas import Notification
from .utils import send_notification
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time notifications.
    1. Accepts WebSocket connections.
    2. Sends a confirmation message upon connection.
    3. Listens for incoming messages and echoes them back.
    4. Handles disconnections and errors gracefully.
    5. Broadcasts disconnection messages to remaining clients.
    """

    logger.debug("WebSocket connection attempt received")
    try:
        await manager.connect(websocket)
        logger.info("WebSocket connection accepted")
        
        try:
            await websocket.send_text("✅ Connection established!")
            while True:
                data = await websocket.receive_text()
                logger.debug(f"Received message: {data}")
                await websocket.send_text(f"Message received: {data}")
                
        except WebSocketDisconnect:
            logger.info("Client disconnected normally")
            manager.disconnect(websocket)
            await manager.broadcast("Client disconnected")
            
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}")
        if websocket in manager.active_connections:
            manager.disconnect(websocket)
    finally:
        if websocket in manager.active_connections:
            manager.disconnect(websocket)
        logger.debug("WebSocket connection cleaned up")

@router.post("/send")
async def send_notification_to_all(notification: Notification, background_tasks: BackgroundTasks):
    """
    Trigger a notification broadcast to all connected WebSocket clients.
    """
    background_tasks.add_task(send_notification, notification)
    return {"message": "Notification broadcast queued"}
