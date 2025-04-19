import yfinance as yf
import logging
import time
import random

logger = logging.getLogger(__name__)

class YahooMarketAdapter:
    def __init__(self):
        self.source = "yahoo"

    def fetch_data(self, symbol, intervals, start_year, end_year):
        logger.info(f" Fetching {symbol} data from Yahoo Finance...")

        ticker_symbol = f"{symbol}=X" if "/" in symbol else symbol  
        ticker = yf.Ticker(ticker_symbol)

        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        
        for interval in intervals: 
         data = ticker.history(start=start_date, end=end_date, interval=interval)
        

        if data.empty:
            logger.error(f" No data fetched for {symbol}.")
            return []

        result = []
        for date, row in data.iterrows():
            result.append({
                "symbol": symbol,
                "source": self.source,
                "interval": intervals,
                "datetime": date.to_pydatetime(),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row.get("Volume", None),
                "trade_count": None,
                "vwap": None,
            })

       
            time.sleep(1)

        logger.info(f" Successfully fetched {len(result)} records for {symbol}.")
        return result
