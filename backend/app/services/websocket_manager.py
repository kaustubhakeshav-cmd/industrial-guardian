import json
from typing import List
from fastapi import WebSocket
from app.data.schemas import TelemetryFrame

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_telemetry(self, frame: TelemetryFrame):
        data_text = frame.model_dump_json()
        for connection in list(self.active_connections):
            try:
                await connection.send_text(data_text)
            except Exception:
                self.disconnect(connection)

ws_manager = ConnectionManager()