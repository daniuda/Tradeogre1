import requests
import hmac
import hashlib
import time
from .base_exchange import BaseExchange

class ProBitExchange(BaseExchange):
    def __init__(self, api_key=None, api_secret=None):
        super().__init__()
        self.base_url = "https://api.probit.com/api/exchange/v1"
        self.api_key = api_key
        self.api_secret = api_secret
    
    def _generate_signature(self, payload):
        """Generează semnătura HMAC pentru cererile autentificate"""
        return hmac.new(
            self.api_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    def get_prices(self):
        """Prețurile curente pentru toate perechile"""
        url = f"{self.base_url}/ticker"
        response = requests.get(url)
        return {
            item['market_id']: float(item['last'])
            for item in response.json()['data']
        }
    
    def get_balance(self):
        """Balanța utilizatorului (necesită auth)"""
        if not self.api_key:
            raise ValueError("API key required for balance check")
        
        timestamp = str(int(time.time() * 1000))
        payload = f"{timestamp}GET/api/exchange/v1/balance"
        signature = self._generate_signature(payload)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Timestamp": timestamp,
            "X-Signature": signature
        }
        
        response = requests.get(
            f"{self.base_url}/balance",
            headers=headers
        )
        return response.json()