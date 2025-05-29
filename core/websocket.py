import asyncio
import json
import logging
from typing import Optional, Dict
from config.settings import Config
from core.logger import setup_logger
from core.database import save_trade

logger = setup_logger("websocket")

try:
    import websockets
    from websockets.exceptions import ConnectionClosed
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False
    logger.error("websockets package not installed. Real-time updates will be disabled.")

class TradeOgreWebsocket:
    def __init__(self):
        self.uri = Config.WEBSOCKET_URI
        self.reconnect_delay = Config.WEBSOCKET_RECONNECT_DELAY
        self.websocket = None
        self.running = False

    async def connect(self) -> bool:
        """Establish websocket connection."""
        if not HAS_WEBSOCKETS:
            return False

        try:
            self.websocket = await websockets.connect(
                self.uri,
                ping_interval=None,
                max_queue=1024,
                close_timeout=1
            )
            logger.info("Websocket connected successfully")
            return True
        except Exception as e:
            logger.error(f"Websocket connection failed: {str(e)}")
            return False

    async def subscribe(self, market: str) -> bool:
        """Subscribe to market updates."""
        if not self.websocket or not HAS_WEBSOCKETS:
            return False

        try:
            subscribe_msg = json.dumps({
                "a": "subscribe",
                "e": "trade",
                "t": market
            })
            await self.websocket.send(subscribe_msg)
            logger.info(f"Subscribed to {market} updates")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to {market}: {str(e)}")
            return False

    async def process_message(self, message: str) -> bool:
        """Process incoming websocket message."""
        try:
            data = json.loads(message)
            
            if data.get('e') == 'trade':
                trade_data = data.get('d', {})
                if not trade_data:
                    return False
                    
                trade = {
                    'id': str(trade_data.get('d', '')),
                    'price': float(trade_data.get('p', 0)),
                    'quantity': float(trade_data.get('q', 0)),
                    'type': 'sell' if trade_data.get('t') == 1 else 'buy'
                }
                
                if not save_trade(trade):
                    logger.warning("Failed to save trade from websocket")
                
                logger.debug(f"Processed trade: {trade}")
                return True
                
        except json.JSONDecodeError:
            logger.error("Failed to decode websocket message")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            
        return False

    async def run(self, market: str):
        """Main websocket loop."""
        if not HAS_WEBSOCKETS:
            logger.warning("Websocket support disabled (package not installed)")
            return

        self.running = True
        logger.info(f"Starting websocket client for {market}")

        while self.running:
            try:
                if not await self.connect():
                    await asyncio.sleep(self.reconnect_delay)
                    continue

                if not await self.subscribe(market):
                    await asyncio.sleep(self.reconnect_delay)
                    continue

                async for message in self.websocket:
                    if not self.running:
                        break
                    await self.process_message(message)

            except ConnectionClosed:
                logger.warning("Websocket connection closed, reconnecting...")
            except Exception as e:
                logger.error(f"Websocket error: {str(e)}")
            finally:
                if self.websocket:
                    await self.websocket.close()
                    self.websocket = None
                
                if self.running:
                    await asyncio.sleep(self.reconnect_delay)

    async def stop(self):
        """Stop the websocket client."""
        self.running = False
        if self.websocket:
            await self.websocket.close()

# Singleton instance
websocket_client = TradeOgreWebsocket()