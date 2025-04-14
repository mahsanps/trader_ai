from market.models import Symbol
import requests


def fetch_and_save_crypto(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Crypto {crypto_id} not found on CoinGecko.")
        return

    data = response.json()

    # Safely access 'is_hidden' with .get() to avoid KeyError
    is_hidden = data.get("is_hidden", False)  # Default to False if 'is_hidden' is not found

    symbol_obj, created = Symbol.objects.get_or_create(
        symbol=data["symbol"].upper(),
        defaults={
            "name": data["name"],
            "sec_id": data["id"],
            "market_type": "spot",
            "exchange": ", ".join([market["market"]["name"] for market in data["tickers"][:3]]),
            "is_active": not is_hidden,  # Use the safely fetched value
            "shares_outstanding": data["market_data"].get("total_supply"),  # Safe fetch for 'total_supply'
            "dividend": None
        }
    )

    if created:
        print(f"✅ {data['name']} ({data['symbol'].upper()}) added to the database.")
    else:
        print(f"⚠ {data['name']} ({data['symbol'].upper()}) already exists in the database.")
