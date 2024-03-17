# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('symbols/', views.get_symbols, name='get_symbols'),
    path('time_series/<str:symbol>/', views.get_time_series, name='get_time_series'),
]
