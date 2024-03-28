from django.core.management.base import BaseCommand
from stocks.utils import parse_alpha_vantage as pav
from stocks.models import BaseStockData, StockPriceData, IncomeStatementData, BalanceSheetData, CashFlowData, EarningsData, QuarterlyStockOverview
from django.conf import settings
import logging
import functools
import json

class Command(BaseCommand):
    help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

    function_to_syncing = {
        'TIME_SERIES_DAILY_ADJUSTED': functools.partial(pav.sync_stock_price_data, interval='daily'),
        'TIME_SERIES_WEEKLY_ADJUSTED': functools.partial(pav.sync_stock_price_data, interval='weekly'),
        'TIME_SERIES_MONTHLY_ADJUSTED': functools.partial(pav.sync_stock_price_data, interval='monthly'),
        'OVERVIEW': pav.sync_base_and_quarterly_overview,  
        'INCOME_STATEMENT': pav.sync_income_statement,
        'BALANCE_SHEET': pav.sync_balance_sheet,
        'CASH_FLOW': pav.sync_cash_flow,
        'EARNINGS': pav.sync_earnings,
    }

    function_to_model = {
        'TIME_SERIES_DAILY_ADJUSTED': StockPriceData,
        'TIME_SERIES_WEEKLY_ADJUSTED': StockPriceData,
        'TIME_SERIES_MONTHLY_ADJUSTED': StockPriceData,
        'INCOME_STATEMENT': IncomeStatementData,
        'BALANCE_SHEET': BalanceSheetData,
        'CASH_FLOW': CashFlowData,
        'EARNINGS': EarningsData,
        # Not adding 'OVERVIEW' here
    }
    
    # functions that have be treated differently in some 
    ts_function_intervals = {
        'TIME_SERIES_DAILY_ADJUSTED': 'daily',
        'TIME_SERIES_WEEKLY_ADJUSTED': 'weekly',
        'TIME_SERIES_MONTHLY_ADJUSTED': 'monthly',
    }

    def add_arguments(self, parser):
        parser.add_argument('function', type=str, help='The function to fetch data for')
        parser.add_argument('--start-index', type=int, help='Start index for stock selection', default=None)
        parser.add_argument('--stop-index', type=int, help='Stop index for stock selection', default=None)
        parser.add_argument(
            '--no-check-exists',
            action='store_false',
            dest='check_exists', 
            help='Do not check if the data already exists in the database'
        )
        parser.add_argument('--outputsize', type=str, help='Specify the output size')
        parser.add_argument('--include-all', action='store_true', help='Include all stocks, not just S&P 500')
        # parser.add_argument(
        #     '--extra-args', 
        #     type=str, 
        #     help='JSON string of extra keyword arguments', 
        #     default='{}'
        # )

    def handle(self, *args, **options):
        function = options['function'].upper()
        start_index = options['start_index']
        stop_index = options['stop_index']
        check_exists = options['check_exists']
        include_all = options['include_all']
        outputsize = options.get('outputsize', None)
        # extra_args = json.loads(options.get('extra-args', '{}'))
        # print("Extra args:", extra_args)  # Debugging line

        if include_all:
            stocks_to_iterate = BaseStockData.objects.all()
        else:
            stocks_to_iterate = BaseStockData.objects.filter(is_sp500=True)
            
        interval = self.ts_function_intervals.get(function)

        stocks_to_iterate = stocks_to_iterate.order_by('symbol')[start_index:stop_index]

        sync_func = self.function_to_syncing.get(function)
        model_class = self.function_to_model.get(function)  

        if not sync_func:
            logging.error(f"No syncing function found for {function}. Please check your mappings.")
            return
          
        for stock in stocks_to_iterate:
            if check_exists and function not in ['OVERVIEW'] + list(self.ts_function_intervals.keys()):
                exists = model_class.objects.filter(stock=stock).exists()
            elif check_exists and function == 'OVERVIEW':
                exists = QuarterlyStockOverview.objects.filter(stock=stock).exists()
            elif check_exists and interval:
                exists = (
                    model_class.objects.
                    filter(stock=stock, interval=interval)
                    .exists()
                )
            else:
                exists = False
                      
            if exists:
                self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
                continue

            try:
                if interval:
                    data = pav.fetch_data(
                        function=function, 
                        stock_symbol=stock.symbol, 
                        api_key=settings.RAPIDAPI_KEY, 
                        interval=interval,
                        outputsize=outputsize
                    )
                else:
                    data = pav.fetch_data(
                        function=function, 
                        stock_symbol=stock.symbol, 
                        api_key=settings.RAPIDAPI_KEY,
                        outputsize=outputsize
                    )
            except Exception as e:
                logging.error(f"Error fetching data for {stock.symbol}: {e}")
                continue
            
            try:
                sync_func(data)
                self.stdout.write(f"Fetched and synced {function} for {stock.symbol}")
            except Exception as e:
                logging.error(f"Error syncing {function} for {stock.symbol}: {e}")
