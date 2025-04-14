import argparse
import requests
from datetime import datetime
import django
import os

# تنظیمات Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trader_ai.settings")
django.setup()

from market.models import News  # Ensure correct path

API_KEY = "PV6FU3BORMPEDOVD"

def fetch_financial_news(ticker, start_year=2023, topic="financial_markets", limit=1000):
    """Akhbar mali baraye yek ticker dar sal mokhassas ro daryaft mikone."""

    time_from = f"{start_year}0101T0000"
    time_to = f"{start_year}1231T2359"

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "market": "forex", 
        "apikey": API_KEY,
        "limit": limit,
        "time_from": time_from,  # Added time_from
        "time_to": time_to       # Added time_to
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()

        # Debugging: Print full response to inspect
        print(" API Response JSON:", data)

        if "feed" in data and data["feed"]:  # Check if feed exists and is not empty
            print(f" Found {len(data['feed'])} news articles.")
            return data["feed"]
        else:
            print(" No news found in API response (empty or missing 'feed').")
            return []
    else:
        print(f" Error {response.status_code}: {response.text}")
        return []


def save_news_to_db(news_list, ticker):
    """ Akhbar ro dar database Django save mikone. """
    saved_count = 0
    for news in news_list:
        title = news.get("title", "No Title")
        url = news.get("url", "")
        summary = news.get("summary", "")
        published_at_str = news.get("time_published", None)

        if published_at_str:
            published_at = datetime.strptime(published_at_str, "%Y%m%dT%H%M%S")
        else:
            published_at = datetime.now()

        if not News.objects.filter(title=title, published_at=published_at).exists():
            News.objects.create(
                ticker=ticker,
                title=title,
                url=url,
                summary=summary,
                published_at=published_at
            )
            saved_count += 1
    
    print(f" Saved {saved_count} news articles for {ticker}.")

def fetch_and_store_news(ticker="AAPL", year=2023):
    """ Akhbar mali yek ticker dar yek sal mokhassas ro daryaft va save mikone. """
    print(f" Fetching news for {ticker} in {year}...")
    news_list = fetch_financial_news(ticker, start_year=year)
    if news_list:
        save_news_to_db(news_list, ticker)
    else:
        print(" No news found to save.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and store financial news")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("year", type=int, help="Year to fetch news for (e.g., 2024)")
    
    args = parser.parse_args()
    print("Arguments:", args)  # Debugging arguments
    fetch_and_store_news(args.ticker, args.year)
