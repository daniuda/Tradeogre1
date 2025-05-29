from abc import ABC, abstractmethod
import logging

class BaseExchange(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def get_prices(self):
        """Fetch current prices"""
        pass
    
    @abstractmethod
    def run(self, notifier):
        """Main monitoring loop"""
        pass