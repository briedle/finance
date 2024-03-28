# urls.py

from django.urls import path
from . import views
# from .views import StockListView

urlpatterns = [
    path('', views.index, name='index'),
    path('symbols/', views.get_symbols, name='get_symbols'),
    path('adjusted_stock_price_ts/<str:symbol>/',
         views.get_adjusted_stock_price_ts, 
         name='get_adjusted_stock_price_ts'
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
]
