from fastapi import WebSocket
from typing import List, Dict
from secrets import token_hex


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[chat_id] = self.connections.get(chat_id, [])
        self.connections[chat_id].append(websocket)

    def disconnect(self, chat_id: str, websocket: WebSocket):
        self.connections[chat_id].remove(websocket)

    async def broadcast(self, chat_id: str, data):
        for connection in self.connections[chat_id]:
            await connection.send_json(data)


def generate_chat_id() -> str:
    return token_hex(8)

