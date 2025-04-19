from django.db import models
from decimal import Decimal

# Create your models here.
def get_default_currency():
    return Currency.objects.get_or_create(currency="USD")[0].id  


class MarketTypeChoices(models.TextChoices):
    STOCK = "Stock", "Stock Market"
    CRYPTO = "Crypto", "Cryptocurrency"
    FOREX = "Forex", "Foreign Exchange"
    COMMODITY = "Commodity", "Commodity Market"
    
class TimeframeChoices(models.TextChoices):
    M1 = "1m", "1 Minute"
    M5 = "5m", "5 Minutes"
    M15 = "15m", "15 Minutes"
    H1 = "1h", "1 Hour"
    D1 = "1d", "1 Day"
    W1 = "1w", "1 Week"
    MN1 = "1mn", "1 Month"

class Currency(models.Model):
    currency =  models.CharField(max_length=200,unique=True)   
    
    def __str__(self):
        return self.currency


class Symbol(models.Model):
    symbol = models.CharField(max_length=100, unique=True)
    currency= models.ForeignKey(Currency,on_delete=models.CASCADE,default=get_default_currency)
    market_type = models.CharField(max_length=100, choices=MarketTypeChoices.choices)  
    sec_id = models.CharField(max_length=255, null=True, blank=True) 
    exchange = models.CharField(max_length=100, null=True, blank=True)  
    is_active = models.BooleanField(default=True)
    related_symbols = models.ManyToManyField("self", blank=True) 
    shares_outstanding = models.BigIntegerField(null=True, blank=True)
    dividend = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return f"{self.symbol}"

class DataSource(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    exchange = models.CharField(max_length=100, null=True, blank=True) 
    data_version = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return f"{self.name} - {self.exchange}"

class MarketData(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)  
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)  
    timeframe = models.CharField(max_length=100, choices=TimeframeChoices.choices, default="1d")  
    datetime = models.DateTimeField()  
    open = models.DecimalField(max_digits=20, decimal_places=8)  
    high = models.DecimalField(max_digits=20, decimal_places=8)  
    low = models.DecimalField(max_digits=20, decimal_places=8)  
    close = models.DecimalField(max_digits=20, decimal_places=8)  
    volume = models.DecimalField(max_digits=20, decimal_places=8)  
    trade_count = models.BigIntegerField(null=True, blank=True)  
    vwap = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)  

    class Meta:
        unique_together = ["symbol", "data_source", "timeframe", "datetime"]  

    @property
    def price(self):
        return self.close

    def __str__(self):
        return f"{self.symbol} - {self.timeframe}"

class News(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, null=True, blank=True)  
    title = models.TextField()
    published_at = models.DateTimeField()
    summary = models.TextField( null=True, blank=True)
    ticker = models.CharField(max_length=1000, null=True, blank=True)
    url = models.URLField(max_length=1000)


    def __str__(self):
        return self.title

class SentimentAnalysis(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, null=True, blank=True)  
    source = models.CharField(max_length=255) 
    text = models.TextField() 
    sentiment_score = models.FloatField() 
    datetime = models.DateTimeField()  

    def __str__(self):
        return f"{self.symbol} - {self.source} ({self.sentiment_score})"

class TechnicalIndicator(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)  
    timeframe = models.CharField(max_length=50, choices=TimeframeChoices.choices)  
    indicator_name = models.CharField(max_length=255)  
    value = models.DecimalField(max_digits=20, decimal_places=8)  
    datetime = models.DateTimeField()  

    def __str__(self):
        return f"{self.symbol} - {self.indicator_name} ({self.value})"

class TradeSignal(models.Model):
    SIGNAL_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('HOLD', 'Hold'),
    ]

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)  
    timeframe = models.CharField(max_length=50, choices=TimeframeChoices.choices)  
    signal_type = models.CharField(max_length=10, choices=SIGNAL_CHOICES)  
    confidence = models.FloatField() 
    reason = models.TextField() 
    datetime = models.DateTimeField()  

    def __str__(self):
        return f"{self.symbol} - {self.signal_type} ({self.confidence}%)"

class TradingStrategy(models.Model):
    name = models.CharField(max_length=255, unique=True)  
    description = models.TextField()  
    parameters = models.JSONField() 

    def __str__(self):
        return self.name

class BacktestResult(models.Model):
    strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE)  
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)  
    timeframe = models.CharField(max_length=50, choices=TimeframeChoices.choices)  
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField()  
    performance_metrics = models.JSONField()  

    def __str__(self):
        return f"{self.strategy} - {self.symbol}"

class ImpactChoices(models.TextChoices):
    HIGH = "High", "High Impact"
    MEDIUM = "Medium", "Medium Impact"
    LOW = "Low", "Low Impact"



class EconomicCalendar(models.Model):
    event_id = models.CharField(max_length=200, unique=True, blank=True, null=True)  
    date = models.DateTimeField()
    time = models.CharField(max_length=100, default="")  
    impact = models.CharField(blank=True, null=True) 
    country = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    event = models.CharField()
    actual = models.CharField(max_length=200, blank=True, null=True)
    previous = models.CharField(max_length=200, blank=True, null=True)  
    forecast = models.CharField(max_length=200, blank=True, null=True)  
    source_url = models.URLField(blank=True, null=True)  
    graph=models.CharField(max_length=50, blank=True, null=True) 
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,default=get_default_currency)  

    def __str__(self):
        return f"{self.event} ({self.impact}) - {self.date}"


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField()
    retweets = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)

    def __str__(self):
        return self.content[:50]
    
    

class COTReport(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    report_date = models.DateField()
    open_interest = models.BigIntegerField()
    commercial_long = models.BigIntegerField()
    commercial_short = models.BigIntegerField()
    non_commercial_long = models.BigIntegerField()
    non_commercial_short = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'report_date')

    def __str__(self):
        return f"{self.symbol} - {self.report_date}"    
    
class FxOptionExpiry(models.Model):
    date = models.DateField(unique=True)
    image = models.ImageField(upload_to='forexlive_images')

    def __str__(self):
        return f"FX Option Expiry - {self.date}"    