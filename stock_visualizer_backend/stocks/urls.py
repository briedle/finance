# urls.py

from django.urls import path
from . import views
# from .views import StockListView

urlpatterns = [
    path('', views.index, name='index'),
    path('symbols/', views.get_symbols, name='get_symbols'),
    path('adjusted_stock_price/<str:symbol>/',
         views.get_adjusted_stock_price, 
         name='get_adjusted_stock_price'
    ),
    path('earnings/<str:symbol>/',
         views.get_earnings, 
         name='get_earnings'
    ),
    path('stocks/', views.stock_list_view, name='stock-list'),
    path('quarterly_overview/<str:symbol>/',
         views.get_quarterly_overview,
         name='get_quarterly_overview'
    ),
    path(
         'balance_sheet/<str:symbol>/',
         views.get_balance_sheet,
           name='get_balance_sheet'
     ),
     path(
           'income_statement/<str:symbol>/',
           views.get_income_statement,
           name='get_income_statement'
     ),
     path(
          'cash_flow/<str:symbol>/',
          views.get_cash_flow,
          name='get_cash_flow'
     ),
     path(
          'earnings_calendar/<str:symbol>/',
          views.get_earnings_calendar,
          name='get_earnings_calendar'
     )
]
