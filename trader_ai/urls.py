
from django.contrib import admin
from django.urls import path
from market_data.views import MarketDataAPIView, NewsAPIView, EconomicCalendarAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("market-data/", MarketDataAPIView.as_view(), name="market-data"),
    path("news/", NewsAPIView.as_view(), name="news"),
    path("economic-calendar/", EconomicCalendarAPIView.as_view(), name="news"),
]
