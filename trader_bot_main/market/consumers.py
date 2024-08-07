import json
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer

class CryptoDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.livecoin_task = asyncio.create_task(self.fetch_live_data())

    async def disconnect(self, close_code):
        await self.livecoin_task.cancel()

    async def fetch_live_data(self):
        uri = "wss://ws-api.livecoinwatch.com/socket.io/?EIO=3&transport=websocket"
        async with websockets.connect(uri) as websocket:
            await websocket.send('420["subscribe",{"frequency":2000,"currency":"USD","stats":true,"coins":{"offset":0,"limit":50,"sort":"rank","order":"ascending","fields":"orderTotal,extremes.all.max.usd,delta.hour,plot.week,cap,volume,delta.day","category":null,"exchanges":null,"platforms":[],"filters":{}},"spotlight":"overview,recent,trending,upvotes","deltas":""}]')
            while True:
                response = await websocket.recv()
                if response.startswith('42'):
                    data = json.loads(response[2:])
                    await self.send(text_data=json.dumps(data))

                # Send "2" to keep connection alive
                await websocket.send("2")
                await asyncio.sleep(3)
