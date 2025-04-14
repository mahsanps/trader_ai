from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from market.models import MarketData, News, EconomicCalendar
from .serializers import MarketDataSerializer, NewsSerializer, EconomicCalendarSerializer
from datetime import datetime
from django.utils.timezone import make_aware

class MarketDataAPIView(APIView):
    def get(self, request):
        symbol = request.query_params.get("symbol") 
        timeframe = request.query_params.get("timeframe") 
        year = request.query_params.get("year")
        start_year = request.query_params.get("start_year")
        end_year = request.query_params.get("end_year")

        queryset = MarketData.objects.all()

        if symbol:
            queryset = queryset.filter(symbol__symbol=symbol) 
        if timeframe:
            queryset = queryset.filter(timeframe=timeframe) 
        if year:
            queryset = queryset.filter(datetime__year=year)
        elif start_year and end_year:
            start_date = make_aware(datetime(int(start_year), 1, 1))
            end_date = make_aware(datetime(int(end_year) + 1, 1, 1))  # تا اول سال بعدی
            queryset = queryset.filter(datetime__gte=start_date, datetime__lt=end_date)

        serializer = MarketDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class NewsAPIView(APIView):
    def get(self, request):
        ticker = request.query_params.get("ticker") 
        title = request.query_params.get("title")
        year = request.query_params.get("year")
        start_year = request.query_params.get("start_year")
        end_year = request.query_params.get("end_year")
        
        

        queryset = News.objects.all()
        if ticker:
            queryset = queryset.filter(ticker=ticker)
        if title:
            queryset = queryset.filter(title__icontains=title)   
            
        if year:
            queryset = queryset.filter( published_at__year=year)
        elif start_year and end_year:
            start_date = make_aware(datetime(int(start_year), 1, 1))
            end_date = make_aware(datetime(int(end_year) + 1, 1, 1))  # تا اول سال بعدی
            queryset = queryset.filter( published_at__gte=start_date,  published_at__lt=end_date)
       

        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    
class EconomicCalendarAPIView(APIView):
    def get(self, request):
        currency = request.query_params.get("currency") 
        event = request.query_params.get("event") 
        year = request.query_params.get("year")
        start_year = request.query_params.get("start_year")
        end_year = request.query_params.get("end_year")

        queryset = EconomicCalendar.objects.all()
        if currency:
            queryset = queryset.filter(currency__currency=currency) 
        if event:
            queryset = queryset.filter(event__icontains=event) 
            
        if year:
            queryset = queryset.filter( date__year=year)
        elif start_year and end_year:
            start_date = make_aware(datetime(int(start_year), 1, 1))
            end_date = make_aware(datetime(int(end_year) + 1, 1, 1))  # تا اول سال بعدی
            queryset = queryset.filter( date__gte=start_date,  date__lt=end_date)
              

        serializer = EconomicCalendarSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
