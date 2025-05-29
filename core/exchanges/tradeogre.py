from .base_exchange import BaseExchange
import requests

class TradeOgreExchange(BaseExchange):
    def __init__(self, api_key=None, api_secret=None):
        super().__init__()
        self.base_url = "https://tradeogre.com/api/v1"
        self.api_key = api_key
        self.api_secret = api_secret
    
    def get_prices(self):
        response = requests.get(f"{self.base_url}/markets")
        return {item['symbol']: item['price'] for item in response.json()}
    
    def get_balance(self):
        # Implementare pentru auth
        pass