from pysupport.utils import setup_django_env
from stocks.utils import parse_alpha_vantage as pav


setup_django_env('/home/briedle/web-projects/finance/stock_visualizer_backend')

api_key = "1c63ffa51amsh98ddb79fb2729e8p14b4fajsn657b83e58886"

stock_symbol = 'MMM'

stock_data = pav.fetch_data(
    stock_symbol, 
    function='TIME_SERIES_MONTHLY_ADJUSTED', 
    api_key=api_key
)
stock_data

pav.sync_monthly_adjusted(stock_data)