# views.py

import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import BaseStockData, MonthlyStockPriceData  # Assuming you have a model for storing stock data


logger = logging.getLogger(__name__)

def get_symbols(request):
    logger.info("Request hit get_symbols")
    symbols = (
        BaseStockData
        .objects
        .values_list('symbol', flat=True)
        .distinct()
    )
    return JsonResponse(list(symbols), safe=False)
    # return JsonResponse({'status': 'ok'})

def get_time_series(request, symbol):
    logger.info("Request hit get_time_series")
    stock_data = (
        MonthlyStockPriceData
        .objects
        .filter(stock__symbol=symbol)
        .values(
            'date', 'open', 'high', 'low', 
            'close', 'adj_close', 'volume', 'dividend'
        )
    )
    return JsonResponse(list(stock_data), safe=False)
    # return JsonResponse({'status': 'ok'})

def index(request):
    logger.info("Request hit index")
    return JsonResponse({'status': 'ok'})

