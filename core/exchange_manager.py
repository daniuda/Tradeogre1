from core.exchanges.probit import ProBitExchange
from core.exchanges.tradeogre import TradeOgreExchange
import importlib

class ExchangeManager:
    def __init__(self):
        self.available_exchanges = {
            'probit': ProBitExchange,
            'tradeogre': TradeOgreExchange
        }
    
    def get_exchange(self, name, *args, **kwargs):
        if name not in self.available_exchanges:
            raise ValueError(f"Exchange {name} not supported. Available: {list(self.available_exchanges.keys())}")
        return self.available_exchanges[name](*args, **kwargs)