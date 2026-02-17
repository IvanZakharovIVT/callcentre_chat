import asyncio

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.core.managers.connection_manager import connection_manager

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("websocket")
    await connection_manager.connect(1, 1, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            # await connection_manager.send_message(f"Сообщение: {data}", websocket)
            await asyncio.sleep(3)
            await connection_manager.broadcast(1, f"Сообщение: {data}", websocket)
    except WebSocketDisconnect:
        connection_manager.disconnect(1, 1)

@router.get("/ping")
async def ping():
    return {"ping": "pong"}
