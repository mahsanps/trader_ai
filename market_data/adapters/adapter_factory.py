from .binance_adapter import BinanceMarketAdapter
from .yahoo_adapter import YahooMarketAdapter


class MarketAdapterFactory:
 
    ADAPTERS = {
        "binance": BinanceMarketAdapter(),
        "yahoo": YahooMarketAdapter(),
      
    }

    @classmethod
    def get_adapter(cls, source: str):
     
        return cls.ADAPTERS.get(source)
