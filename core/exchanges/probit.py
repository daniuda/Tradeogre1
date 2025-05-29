import requests
import time
from .base_exchange import BaseExchange

class ProBitExchange(BaseExchange):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.probit.com/api/exchange/v1"
    
    def get_prices(self):
        try:
            response = requests.get(f"{self.base_url}/ticker")
            return {
                item['market_id']: float(item['last'])
                for item in response.json()['data']
            }
        except Exception as e:
            self.logger.error(f"Error fetching prices: {str(e)}")
            return None
    
    def run(self, notifier):
        while True:
            prices = self.get_prices()
            if prices:
                message = "📈 <b>ProBit Prices</b>\n"
                message += "\n".join([f"{pair}: {price}" for pair, price in list(prices.items())[:10]])  # Show first 10 pairs
                notifier.send(message)
            time.sleep(60)