import logging
import asyncio
from config.settings import Config
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot = None
        self.loop = asyncio.new_event_loop()
        self._initialize_bot()

    def _initialize_bot(self):
        try:
            from telegram import Bot
            if not Config.TELEGRAM_BOT_TOKEN:
                raise ValueError("Missing Telegram token")
            self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
            logger.info("Telegram bot initialized")
        except ImportError:
            logger.error("python-telegram-bot not installed")
        except Exception as e:
            logger.error(f"Bot init failed: {e}")

    async def _send_async(self, message):
        try:
            await self.bot.send_message(
                chat_id=Config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="Markdown"
            )
            return True
        except TelegramError as e:
            logger.error(f"Telegram API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return False

    def send_alert(self, message):
        if not self.bot:
            logger.warning("Bot not initialized")
            return False
            
        try:
            return self.loop.run_until_complete(self._send_async(message))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

telegram_notifier = TelegramNotifier()