import threading
import time
from web.app import app
from core.database import init_db
from core.telegram import telegram_notifier
from core.tradeogre import get_recent_trades  # This was missing
from config.settings import Config
from core.logger import setup_logger

logger = setup_logger("main")

# Add this at the top
import asyncio

# Update the TradeMonitor class
class TradeMonitor:
    def __init__(self):
        self.last_trade_id = None
        self.loop = asyncio.new_event_loop()

    def check_trades(self):
        try:
            trades = get_recent_trades()
            if trades and trades[0]['id'] != self.last_trade_id:
                trade = trades[0]
                self.last_trade_id = trade['id']
                
                message = (
                    f"🔄 *New Trade on {Config.TRADE_PAIR}*\n"
                    f"💰 Price: `{trade['price']:.8f}` USDT\n"
                    f"📊 Amount: `{trade['quantity']:.4f}` VTC\n"
                    f"💵 Value: `${trade['price'] * trade['quantity']:.2f}`"
                )
                
                # Use the synchronous wrapper
                if not telegram_notifier.send_alert(message):
                    logger.warning("Failed to send Telegram alert")

        except Exception as e:
            logger.error(f"Error checking trades: {e}")
            raise

    def run(self):
        """Main monitoring loop"""
        logger.info(f"Starting trade monitor for {Config.TRADE_PAIR}")
        while True:
            try:
                self.check_trades()
                time.sleep(Config.POLL_INTERVAL)
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(min(60, Config.POLL_INTERVAL * 2))  # Backoff

def run_flask():
    """Run Flask web server"""
    try:
        logger.info(f"Starting web server on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
        app.run(
            host=Config.FLASK_HOST,
            port=Config.FLASK_PORT,
            use_reloader=False
        )
    except Exception as e:
        logger.critical(f"Web server failed: {e}")
        raise

if __name__ == '__main__':
    try:
        # Verify configuration
        Config.verify()
        
        # Initialize components
        init_db()
        telegram_notifier.send_alert("🚀 Trade monitor starting...")
        
        # Start threads
        monitor = TradeMonitor()
        threads = [
            threading.Thread(target=monitor.run, daemon=True),
            threading.Thread(target=run_flask, daemon=True)
        ]
        
        for t in threads:
            t.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        telegram_notifier.send_alert("⚠️ Trade monitor shutting down")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        telegram_notifier.send_alert(f"❌ Trade monitor crashed: {str(e)[:100]}")
    finally:
        logger.info("Clean shutdown complete")