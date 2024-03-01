import asyncio
import websockets
import json
from dotenv import load_dotenv
import os


load_dotenv()

class MyServer:
    # TODO: CRUD for messages
    async def request_handler(self, request):
        ...
    async def __aenter__(self):
        print("ENTER async with")
        async with websockets.serve(self.request_handler,  os.getenv("WS_HOST"), os.getenv("WS_PORT")):
            await asyncio.Future()
        print("~ENTER async with")
    async def __aexit__(self, *args):
        print("EXIT async with")

async def main():
    async with MyServer() as server:
        print(server)

if __name__ == "__main__":
    asyncio.run(main())
