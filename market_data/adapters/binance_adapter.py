import requests
import pandas as pd
import time
import logging
from .base_adapter import BaseMarketAdapter
from market.models import Symbol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceMarketAdapter(BaseMarketAdapter):
    BASE_URL = "https://api.binance.com/api/v3/klines"

    def fetch_data(self, symbol, intervals=["1d"], start_year=2020, end_year=2024):
        all_data = []

        for interval in intervals:
            for year in range(start_year, end_year + 1):
                start_time = int(pd.Timestamp(f"{year}-01-01").timestamp() * 1000)
                end_time = int(pd.Timestamp(f"{year}-12-31").timestamp() * 1000)

                while start_time < end_time:
                    params = {
                        "symbol": symbol,
                        "interval": interval,
                        "startTime": start_time,
                        "limit": 1000
                    }

                    response = requests.get(self.BASE_URL, params=params)
                    if response.status_code != 200:
                        logger.warning(f"⚠ Error fetching {interval} data: {response.text}")
                        break

                    data = response.json()
                    if not data:
                        break

                  
                    parsed_data = self.parse_data(data, symbol, interval)
                    all_data.extend(parsed_data)

                    start_time = data[-1][0] + 1  # جلوگیری از دریافت داده‌های تکراری
                    time.sleep(1)  # جلوگیری از بلاک شدن

        return all_data

    def parse_data(self, raw_data, symbol, interval):
       
        parsed_data = []
        for row in raw_data:
            parsed_data.append({
                "source": "binance",
                "symbol": symbol,
                "interval": interval,
                "datetime": pd.to_datetime(row[0], unit="ms"),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
                "trade_count": float(row[8]), 
                "vwap": (float(row[7]) if row[7] else None)  
            })
        return parsed_data


