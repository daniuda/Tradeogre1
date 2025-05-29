import threading
import logging
from core.exchanges.tradeogre import TradeOgreExchange
from core.exchanges.probit import ProBitExchange
from core.notification import TelegramNotifier
from web.app import app
from config.settings import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_flask():
    try:
        app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT)
    except Exception as e:
        logger.error(f"Flask error: {str(e)}")

if __name__ == "__main__":
    try:
        notifier = TelegramNotifier()
        
        # Initialize exchanges
        exchanges = [
            TradeOgreExchange(),
            ProBitExchange()
        ]
        
        # Start monitoring threads
        threads = []
        for exchange in exchanges:
            thread = threading.Thread(
                target=exchange.run,
                args=(notifier,),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        
        # Start web interface
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")