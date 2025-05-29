from .tradeogre import TradeOgreExchange
from .binance import BinanceExchange
from .kraken import KrakenExchange

class ExchangeManager:
    def __init__(self):
        self.exchanges = {
            'tradeogre': TradeOgreExchange,
            'binance': BinanceExchange,
            'kraken': KrakenExchange
        }
    
    def get_exchange(self, name, *args, **kwargs):
        if name not in self.exchanges:
            raise ValueError(f"Exchange {name} not supported")
        return self.exchanges[name](*args, **kwargs)