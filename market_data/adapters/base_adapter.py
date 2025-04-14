from abc import ABC, abstractmethod

class BaseMarketAdapter(ABC):
  
    
    @abstractmethod
    def fetch_data(self, symbol: str):
  
        pass
    
    @abstractmethod
    def parse_data(self, raw_data: dict):
      
        pass
