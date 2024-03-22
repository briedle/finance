# from pysupport.utils import setup_django_env
from stocks.utils import parse_alpha_vantage as pav
from django.conf import settings
from stocks.models import BaseStockData#, MonthlyStockPriceData


stocks_to_iterate = BaseStockData.objects.all()[10:50]

# for stock in stocks_to_iterate:
    
# symbols = [stock.symbol for stock in stocks_to_iterate]    

fetched_data = [
    pav.fetch_data(
        stock.symbol,
        function='TIME_SERIES_MONTHLY_ADJUSTED',
        api_key=settings.RAPIDAPI_KEY
    )
    for stock in stocks_to_iterate
]

for data in fetched_data:
    pav.sync_monthly_adjusted(data)
# import environ
# from pathlib import Path

# Initialize environment variables
# env = environ.Env()
# # Assuming your script is in stock_visualizer_backend/experimental
# # and your .env file is in stock_visualizer_backend/
# BASE_DIR = Path(__file__).resolve().parent.parent
# env_file = str(BASE_DIR / '.env')
# env.read_env(env_file)

# # Access environment variables
# API_KEY = env('RAPIDAPI_KEY')

# setup_django_env('/home/briedle/web-projects/finance/stock_visualizer_backend')

# stock_symbol = 'MMM'
# print(stock_symbol)
# stock_data = pav.fetch_data(
#     stock_symbol, 
#     function='TIME_SERIES_MONTHLY_ADJUSTED', 
#     api_key=settings.RAPIDAPI_KEY
# )

# print(stock_data)

