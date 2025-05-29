import requests
import time
from .base_exchange import BaseExchange

class TradeOgreExchange(BaseExchange):
    def __init__(self):
        super().__init__()
        self.base_url = "https://tradeogre.com/api/v1"
    
    def get_prices(self):
        try:
            response = requests.get(f"{self.base_url}/markets")
            data = response.json()
            
            # TradeOgre now returns a list of markets
            if isinstance(data, list):
                return {item['market']: float(item['price']) for item in data}
            # Fallback to old structure if needed
            elif isinstance(data, dict):
                return {market: float(info['price']) for market, info in data.items()}
            else:
                self.logger.error("Unexpected API response format")
                return None
                
        except Exception as e:
            self.logger.error(f"Error fetching prices: {str(e)}")
            return None
    
    def run(self, notifier):
        while True:
            prices = self.get_prices()
            if prices:
                message = "📊 <b>TradeOgre Prices</b>\n"
                message += "\n".join([f"{pair}: {price}" for pair, price in prices.items()][:10])  # Show first 10 pairs
                notifier.send(message)
            time.sleep(60)