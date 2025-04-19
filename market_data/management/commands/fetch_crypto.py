from django.core.management.base import BaseCommand
from market_data.adapters.coingecko_adapter import fetch_and_save_crypto

class Command(BaseCommand):
    help = "Fetch and save crypto market data"

    def add_arguments(self, parser):
        parser.add_argument("symbols", nargs="+", type=str, help="List of crypto symbols")

    def handle(self, *args, **options):
        symbols = options["symbols"]
        for symbol in symbols:
            self.stdout.write(f" Fetching market data for {symbol}...")
            try:
                fetch_and_save_crypto(symbol)
                self.stdout.write(self.style.SUCCESS(f" Successfully saved data for {symbol}."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f" Error fetching data for {symbol}: {e}"))
