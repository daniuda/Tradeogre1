from .tradeogre import TradeOgreExchange
from .binance import BinanceExchange
from .kraken import KrakenExchange
from .probit import ProBitExchange  # Adăugăm importul

class ExchangeManager:
    def __init__(self):
        self.exchanges = {
            'tradeogre': TradeOgreExchange,
            'binance': BinanceExchange,
            'kraken': KrakenExchange,
            'probit': ProBitExchange  # Adăugăm noul exchange
        }
    # ... restul codului rămâne neschimbat ...
class ExchangeManager:from .probit import ProBitExchange  # Adăugăm importul

class ExchangeManager:
    def __init__(self):
        self.exchanges = {
            'tradeogre': TradeOgreExchange,
            'binance': BinanceExchange,
            'kraken': KrakenExchange,
            'probit': ProBitExchange  # Adăugăm noul exchange
        }
        
    def get_exchange(self, name, *args, **kwargs):
        if name not in self.exchanges:
            raise ValueError(f"Exchange {name} not supported")
        return self.exchanges[name](*args, **kwargs)