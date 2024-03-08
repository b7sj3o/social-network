import asyncio
import websockets
import json
from dotenv import load_dotenv
import os


load_dotenv()

sockets = set()
messages = []

class MyServer:
    async def request_handler(self, request):
        async for message in request:
            sockets.add(request)
            msg = json.loads(message)
            uuid = msg.get('sender')
            text = msg.get('text')
            messages.append({'uuid': uuid, 'text': text })
            for sock in filter(lambda x: x != request, sockets):
                await sock.send(json.dumps({'uuid': uuid, 'text': text }))

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