from rest_framework import serializers
from market.models import MarketData, News, EconomicCalendar

class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"
        

class EconomicCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicCalendar
        fields = "__all__"        