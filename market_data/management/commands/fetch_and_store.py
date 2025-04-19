from django.core.management.base import BaseCommand
from market_data.services.fetch_market_data import fetch_market_data, save_market_data

class Command(BaseCommand):
    help = "Fetch and store market data from a given source"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="Data source (e.g., binance)")
        parser.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
        parser.add_argument(
            "--timeframes",
            nargs="+",
            default=["1d"],
            help="List of timeframes (e.g., 1d 4h 1h)"
        )
        parser.add_argument("--start_year", type=int, default=2020, help="Start year for data fetching")
        parser.add_argument("--end_year", type=int, default=2024, help="End year for data fetching")

    def handle(self, *args, **options):
        source = options["source"]
        symbol = options["symbol"]
        timeframes = options["timeframes"]
        start_year = options["start_year"]
        end_year = options["end_year"]

       
        data_list = fetch_market_data(source, symbol, timeframes, start_year, end_year)

        if data_list:
            print(" Calling save_market_data now...")
            save_market_data(data_list)
           
        else:
            print(" No data fetched.")
