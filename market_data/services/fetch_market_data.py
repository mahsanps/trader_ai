import logging
from market_data.adapters.adapter_factory import MarketAdapterFactory
from market.models import Symbol, MarketData, DataSource
from datetime import timedelta, datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_market_data(source, symbol, intervals, start_year=2020, end_year=2024):
    
    adapter = MarketAdapterFactory.get_adapter(source)
    if not adapter:
        raise ValueError(f"❌ No adapter found for source: {source}")

    logger.info(f"📌 Fetching data for {symbol} from {source}...")
    all_data = adapter.fetch_data(symbol, intervals, start_year, end_year)

    logger.info(f"✅ Fetched {len(all_data)} records.")
   
    return all_data

def save_market_data(all_data):
   
    if not all_data:
        logger.warning("⚠ No data to save.")
        return

    objects_to_create = []
    
    for data in all_data:
        symbol = data["symbol"]
        
        symbol_instance, created = Symbol.objects.get_or_create(symbol=symbol)

        data_source, _ = DataSource.objects.get_or_create(name=data["source"])
        timeframe = data["interval"]  

        exists = MarketData.objects.filter(
            symbol=symbol_instance, 
            data_source=data_source,
            timeframe=timeframe,
            datetime=data["datetime"]
        ).exists()

        if exists:
            logger.warning(f"⚠ Data for {data['symbol']} at {data['datetime']} ({timeframe}) already exists. Skipping...")
            continue  

        objects_to_create.append(
            MarketData(
                symbol=symbol_instance, 
                data_source=data_source,
                timeframe=timeframe,
                datetime=data["datetime"],
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
                volume=data["volume"],
                trade_count=data["trade_count"],
                vwap=data["vwap"]
            )
        )

    if objects_to_create:
        MarketData.objects.bulk_create(objects_to_create, ignore_conflicts=True)
        logger.info(f"✅ Successfully saved {len(objects_to_create)} records.")
    else:
        logger.warning("⚠ No new data to save.")
