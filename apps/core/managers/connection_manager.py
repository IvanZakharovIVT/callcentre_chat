from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        # chat_id -> {user_id -> websocket}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, chat_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket

    def disconnect(self, chat_id: str, user_id: str):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].pop(user_id, None)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id: str, message: dict, exclude_user: str = None):
        if chat_id in self.active_connections:
            for user_id, connection in self.active_connections[chat_id].items():
                if exclude_user and user_id == exclude_user:
                    continue
                try:
                    await connection.send_json(message)
                except:
                    pass  # Connection dead, will be cleaned up on next disconnect

connection_manager = ConnectionManager()
