from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    # accepts and stores a client connection
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # removes it when a client leaves
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # sends a message to a specific client
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # sends a message to everyone
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
