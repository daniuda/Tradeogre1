import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-default-key")

    # Database
    DATABASE_FILE = "trades.db"
    
    # TradeOgre
    TRADE_PAIR = "VTC-USDT"
    POLL_INTERVAL = 60
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Logging
    LOG_FILE = "vtc_monitor.log"

    PROBIT_API_KEY = ""  # Completează în .env
    PROBIT_API_SECRET = ""  # Tratează ca informație sensibilă!

    @classmethod
    def verify(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("Missing Telegram bot token")
        if not cls.TELEGRAM_CHAT_ID:
            raise ValueError("Missing Telegram chat ID")