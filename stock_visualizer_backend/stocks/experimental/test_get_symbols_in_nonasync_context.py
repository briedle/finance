from pysupport.utils import setup_django_env


setup_django_env('/home/briedle/web-projects/finance/stock_visualizer_backend')


from django.shortcuts import render
from django.http import JsonResponse
from stocks.models import BaseStockData  # Assuming you have a model for storing stock data

def get_symbols(request):
    symbols = (
        BaseStockData
        .objects
        .values_list('symbol', flat=True)
        .distinct()
    )
    return JsonResponse(list(symbols), safe=False)

def get_symbols_data():
    symbols = (
        BaseStockData
        .objects
        .values_list('symbol', flat=True)
        .distinct()
    )
    return list(symbols)


print(get_symbols(2))
print(get_symbols_data())