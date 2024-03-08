import json
import websockets
from websockets.legacy.protocol import WebSocketCommonProtocol
import asyncio
from dotenv import load_dotenv
from os import getenv

load_dotenv()
CONNECTIONS = {}

async def register(websocket):
    # CONNECTIONS[websocket] = None
    try:
        await websocket.wait_closed()
        await broadcast_messages(websocket)
    finally:
        # CONNECTIONS.pop(websocket)
        ...
async def broadcast_messages(websocket:WebSocketCommonProtocol):
    while True:
        message = await websocket.recv() # Receive
        data = json.loads(message)
        sender = data.get('sender')
        recipient = data.get('recipient')

        if sender == recipient:
            CONNECTIONS[sender] = websocket
        else:
            await CONNECTIONS[recipient].send(message)

        print(f"{CONNECTIONS=}")

        await asyncio.sleep(1)
        
async def main():
    async with websockets.serve(register, getenv("WS_HOST"), getenv("WS_PORT") ):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
