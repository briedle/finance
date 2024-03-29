# views.py

import logging
from django.shortcuts import render
from django.http import JsonResponse
# from .models import BaseStockData, StockPriceData 
# from rest_framework.views import APIView
# from rest_framework.response import Response
from . import models 
# from .serializers import StockSerializer
from django.core import serializers

# class StockListView(APIView):
#     def get(self, request):
#         stocks = (
#             BaseStockData.objects
#             .values('symbol', 'name')
#             .distinct()
#             .order_by('name')
#         )
#         stocks = list(stocks)
#         # Serialize the queryset manually to JSON
#         stocks_json = serializers.serialize('json', stocks)
#         # Return an HttpResponse with content_type as 'application/json'
#         return JsonResponse(stocks_json, safe=False, content_type='application/json')
#         # serializer = StockSerializer(stocks, many=True)
#         # return Response(serializer.data)
logger = logging.getLogger(__name__)

def index(request):
    logger.info("Request hit index")
    return JsonResponse({'status': 'ok'})

def stock_list_view(request):
    # Assuming you want a unique list based on 'symbol'
    stocks = (
        models.BaseStockData.objects
        .filter(is_sp500=True)
        .values('symbol', 'name')
        .distinct()
        .order_by('name')
    )
    # Convert to list to make it serializable as JSON
    stocks_list = list(stocks)
    # Return response
    return JsonResponse(stocks_list, safe=False)


def get_symbols(request):
    logger.info("Request hit get_symbols")
    symbols = (
        models.BaseStockData
        .objects
        .filter(is_sp500=True)
        .values_list('name', flat=True)
        .distinct()
        .order_by('name')
    )
    return JsonResponse(list(symbols), safe=False)
    # return JsonResponse({'status': 'ok'})

def get_adjusted_stock_price(request, symbol):
    logger.info("Request hit get_time_series")
    stock_data = (
        # MonthlyStockPriceData
        models.StockPriceData
        .objects
        .filter(
            stock__symbol=symbol,
            interval='daily'
        )
        .values(
            'date', 'open', 'high', 'low', 
            'close', 'adj_close', 'volume', 'dividend'
        )
        .order_by('date')
    )
    return JsonResponse(list(stock_data), safe=False)
    # return JsonResponse({'status': 'ok'})
    
def get_quarterly_overview(request, symbol):
    logger.info("Request hit get_quarterly_overview")
    stock_data = (
        models.QuarterlyStockOverview
        .objects
        .filter(stock__symbol=symbol)
      .values(
          'stock__name', 
          'stock__symbol', 
          *{f.name for f in models.QuarterlyStockOverview._meta.get_fields()}
      )
    )
    return JsonResponse(list(stock_data), safe=False)
    # return JsonResponse({'status': 'ok'})
    
def get_earnings(request, symbol):
    stock_data = (
        models.EarningsData
        .objects
        .filter(stock__symbol=symbol,
                report_type='quarterly')
      .values(
            'fiscal_date_ending', 
            'reported_eps', 
            # 'estimated_eps', 
            # 'surprise', 
            'surprise_percentage'
      )
      .order_by('fiscal_date_ending')
    )
    return JsonResponse(list(stock_data), safe=False)


def get_balance_sheet(request, symbol):
    stock_data = (
        models.BalanceSheetData
        .objects
        .filter(stock__symbol=symbol,
                report_type='quarterly')
      .values()
      .order_by('date')
    )
    return JsonResponse(list(stock_data), safe=False)


def get_income_statement(request, symbol):
    stock_data = (
        models.IncomeStatementData
        .objects
        .filter(stock__symbol=symbol,
                report_type='quarterly')
        .values()
        .order_by('date')
    )
    return JsonResponse(list(stock_data), safe=False)


def get_cash_flow(request, symbol):
    logger.info("Request hit get_cash_flow")
    stock_data = (
        models.CashFlowData
        .objects
        .filter(stock__symbol=symbol,
                report_type='quarterly')
        .values()
        .order_by('date')
    )
    return JsonResponse(list(stock_data), safe=False)


def get_earnings_calendar(request, symbol):
    stock_data = (
        models.EarningsCalendarData
        .objects
        .filter(stock__symbol=symbol)
        .values()
        .order_by('fiscal_date_ending')
    )
    return JsonResponse(list(stock_data), safe=False)


def get_base_data(request, symbol):
    stock_data = (
        models.BaseStockData
        .objects
        .filter(symbol=symbol)
        .values()
    )
    return JsonResponse(list(stock_data), safe=False)