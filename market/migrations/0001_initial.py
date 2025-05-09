# Generated by Django 5.1.7 on 2025-04-18 14:09

import django.db.models.deletion
import market.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('exchange', models.CharField(blank=True, max_length=100, null=True)),
                ('data_version', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='FxOptionExpiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('image', models.ImageField(upload_to='forexlive_images')),
            ],
        ),
        migrations.CreateModel(
            name='TradingStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('parameters', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('retweets', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('replies', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EconomicCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('date', models.DateTimeField()),
                ('time', models.CharField(default='', max_length=100)),
                ('impact', models.CharField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('event', models.CharField()),
                ('actual', models.CharField(blank=True, max_length=200, null=True)),
                ('previous', models.CharField(blank=True, max_length=200, null=True)),
                ('forecast', models.CharField(blank=True, max_length=200, null=True)),
                ('source_url', models.URLField(blank=True, null=True)),
                ('graph', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.ForeignKey(default=market.models.get_default_currency, on_delete=django.db.models.deletion.CASCADE, to='market.currency')),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=100, unique=True)),
                ('market_type', models.CharField(choices=[('Stock', 'Stock Market'), ('Crypto', 'Cryptocurrency'), ('Forex', 'Foreign Exchange'), ('Commodity', 'Commodity Market')], max_length=100)),
                ('sec_id', models.CharField(blank=True, max_length=255, null=True)),
                ('exchange', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('shares_outstanding', models.BigIntegerField(blank=True, null=True)),
                ('dividend', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('currency', models.ForeignKey(default=market.models.get_default_currency, on_delete=django.db.models.deletion.CASCADE, to='market.currency')),
                ('related_symbols', models.ManyToManyField(blank=True, to='market.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='SentimentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('sentiment_score', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('symbol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('summary', models.TextField(blank=True, null=True)),
                ('ticker', models.CharField(blank=True, max_length=1000, null=True)),
                ('url', models.URLField()),
                ('symbol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalIndicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', models.CharField(choices=[('1m', '1 Minute'), ('5m', '5 Minutes'), ('15m', '15 Minutes'), ('1h', '1 Hour'), ('1d', '1 Day'), ('1w', '1 Week'), ('1mn', '1 Month')], max_length=50)),
                ('indicator_name', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=8, max_digits=20)),
                ('datetime', models.DateTimeField()),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='TradeSignal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', models.CharField(choices=[('1m', '1 Minute'), ('5m', '5 Minutes'), ('15m', '15 Minutes'), ('1h', '1 Hour'), ('1d', '1 Day'), ('1w', '1 Week'), ('1mn', '1 Month')], max_length=50)),
                ('signal_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell'), ('HOLD', 'Hold')], max_length=10)),
                ('confidence', models.FloatField()),
                ('reason', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='BacktestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', models.CharField(choices=[('1m', '1 Minute'), ('5m', '5 Minutes'), ('15m', '15 Minutes'), ('1h', '1 Hour'), ('1d', '1 Day'), ('1w', '1 Week'), ('1mn', '1 Month')], max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('performance_metrics', models.JSONField()),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.tradingstrategy')),
            ],
        ),
        migrations.CreateModel(
            name='MarketData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', models.CharField(choices=[('1m', '1 Minute'), ('5m', '5 Minutes'), ('15m', '15 Minutes'), ('1h', '1 Hour'), ('1d', '1 Day'), ('1w', '1 Week'), ('1mn', '1 Month')], default='1d', max_length=100)),
                ('datetime', models.DateTimeField()),
                ('open', models.DecimalField(decimal_places=8, max_digits=20)),
                ('high', models.DecimalField(decimal_places=8, max_digits=20)),
                ('low', models.DecimalField(decimal_places=8, max_digits=20)),
                ('close', models.DecimalField(decimal_places=8, max_digits=20)),
                ('volume', models.DecimalField(decimal_places=8, max_digits=20)),
                ('trade_count', models.BigIntegerField(blank=True, null=True)),
                ('vwap', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.datasource')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
            ],
            options={
                'unique_together': {('symbol', 'data_source', 'timeframe', 'datetime')},
            },
        ),
        migrations.CreateModel(
            name='COTReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField()),
                ('open_interest', models.BigIntegerField()),
                ('commercial_long', models.BigIntegerField()),
                ('commercial_short', models.BigIntegerField()),
                ('non_commercial_long', models.BigIntegerField()),
                ('non_commercial_short', models.BigIntegerField()),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.symbol')),
            ],
            options={
                'unique_together': {('symbol', 'report_date')},
            },
        ),
    ]
