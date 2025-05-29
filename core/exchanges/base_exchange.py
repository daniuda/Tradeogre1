from abc import ABC, abstractmethod
import logging

class BaseExchange(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def get_prices(self):
        """Returnează un dicționar cu prețurile"""
        pass
    
    @abstractmethod
    def get_balance(self):
        """Returnează balanța utilizatorului"""
        pass