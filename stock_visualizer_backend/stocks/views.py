from django.shortcuts import render
from django.http import JsonResponse
from .models import StockData  # Assuming you have a model for storing stock data

def get_symbols(request):
    symbols = (
        StockData
        .objects
        .values_list('symbol', flat=True)
        .distinct()
    )
    return JsonResponse(list(symbols), safe=False)

def get_time_series(request, symbol):
    stock_data = (
        StockData
        .objects
        .filter(symbol=symbol)
        .values(
            'date', 'open', 'high', 'low', 
            'close', 'adj_close', 'volume', 'dividend'
        )
    )
    return JsonResponse(list(stock_data), safe=False)


