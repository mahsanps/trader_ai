from django.contrib import admin
from .models import Symbol, MarketData, DataSource, EconomicCalendar, News, COTReport,FxOptionExpiry

class MarketDataInline(admin.TabularInline):  
    model = MarketData
    extra = 1  


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("symbol", "market_type")
    list_filter = ("market_type", "currency")
    inlines = [MarketDataInline] 

admin.site.register(MarketData)
admin.site.register(DataSource)
admin.site.register(EconomicCalendar)
admin.site.register(News)
admin.site.register(COTReport)
admin.site.register(FxOptionExpiry)
