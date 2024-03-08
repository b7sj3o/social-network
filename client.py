import websockets
import asyncio
from dotenv import load_dotenv
from os import getenv

load_dotenv()


async def hello():
    uri = f"ws://{getenv('WS_HOST')}:{getenv('WS_PORT')}"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")

        # await websocket.send(name)
        # print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())