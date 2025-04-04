import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trader_ai.settings')
django.setup()


from market.models import Tweet 
from datetime import datetime


with open('btc_tweets.json', 'r', encoding='utf-8') as f:
    tweets = json.load(f)

   
    for tweet in tweets:
        Tweet.objects.get_or_create(
            tweet_id=tweet['id'],
            text=tweet['content'],
            username=tweet['user']['username'],
            created_at=datetime.fromtimestamp(tweet['date']),
            hashtags=','.join([hashtag['tag'] for hashtag in tweet['hashtags']]),
            likes=tweet['likeCount'],
            retweets=tweet['repostCount']
        )
