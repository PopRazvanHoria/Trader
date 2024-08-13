import json
import asyncio
import websockets
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class CryptoDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection accepted.")
        self.livecoin_task = asyncio.create_task(self.fetch_live_data())

    async def disconnect(self, close_code):
        logger.info("WebSocket connection closed.")
        await self.livecoin_task.cancel()

    async def fetch_live_data(self):
        uri = "wss://ws-api.livecoinwatch.com/socket.io/?EIO=3&transport=websocket"
        try:
            async with websockets.connect(uri) as websocket:
                logger.info("Connected to WebSocket.")                
                # await self.send("TEDS1")
                await websocket.send('420["subscribe",{"frequency":2200,"currency":"USD","stats":true,"coins":{"offset":0,"limit":50,"sort":"rank","order":"ascending","fields":"orderTotal,extremes.all.max.usd,delta.hour,plot.week,cap,volume,delta.day","category":null,"exchanges":null,"platforms":[],"filters":{}},"spotlight":"overview,recent,trending,upvotes","deltas":""}]')
                logger.info("Subscription message sent.")
                while True:
                    response = await websocket.recv()
                    logger.info(f"Received response: {response}")
                    if response.startswith('42'):
                        data = json.loads(response[2:])
                        await self.send(text_data=json.dumps(data))

                    # Send "2" to keep connection alive
                    await websocket.send("2")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
