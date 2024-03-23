from django.core.management.base import BaseCommand
from stocks.utils import parse_alpha_vantage as pav
from stocks.models import BaseStockData, MonthlyStockPriceData, IncomeStatementData, BalanceSheetData, CashFlowData, EarningsData, QuarterlyStockOverview
from django.conf import settings
import logging

class Command(BaseCommand):
    help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

    function_to_syncing = {
        'TIME_SERIES_MONTHLY_ADJUSTED': pav.sync_monthly_adjusted,
        'INCOME_STATEMENT': pav.sync_income_statement,
        'BALANCE_SHEET': pav.sync_balance_sheet,
        'OVERVIEW': pav.sync_base_and_quarterly_overview,  
        'CASH_FLOW': pav.sync_cash_flow,
        'EARNINGS': pav.sync_earnings,
    }

    # For this special case, we'll handle the existence check differently
    function_to_model = {
        'TIME_SERIES_MONTHLY_ADJUSTED': MonthlyStockPriceData,
        'INCOME_STATEMENT': IncomeStatementData,
        'BALANCE_SHEET': BalanceSheetData,
        'CASH_FLOW': CashFlowData,
        'EARNINGS': EarningsData,
        # Not adding 'OVERVIEW' here
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
        parser.add_argument('--include-all', action='store_true', help='Include all stocks, not just S&P 500')

    def handle(self, *args, **options):
        function = options['function'].upper()
        start_index = options['start_index']
        stop_index = options['stop_index']
        check_exists = options['check_exists']
        include_all = options['include_all']

        if include_all:
            stocks_to_iterate = BaseStockData.objects.all()
        else:
            stocks_to_iterate = BaseStockData.objects.filter(is_sp500=True)

        stocks_to_iterate = stocks_to_iterate.order_by('symbol')[start_index:stop_index]

        sync_func = self.function_to_syncing.get(function)
        model_class = self.function_to_model.get(function)  

        if not sync_func:
            self.stdout.write(f"No syncing function found for {function}. Please check your mappings.")
            return

        for stock in stocks_to_iterate:
            if check_exists and function != 'OVERVIEW':
                exists = model_class.objects.filter(stock=stock).exists()   
                if exists:
                    self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
                    continue

            # Custom check for OVERVIEW since it involves two models
            if check_exists and function == 'OVERVIEW':
                overview_exists = QuarterlyStockOverview.objects.filter(stock=stock).exists()
                if overview_exists:
                    self.stdout.write(f"Quarterly overview data for {stock.symbol} already exists. Skipping API call.")
                    continue

            try:
                data = pav.fetch_data(function=function, stock_symbol=stock.symbol, api_key=settings.RAPIDAPI_KEY)
            except Exception as e:
                logging.error(f"Error fetching data for {stock.symbol}: {e}")
                continue
            
            try:
                sync_func(data)
                self.stdout.write(f"Fetched and synced data for {stock.symbol} using {sync_func.__name__}")
            except Exception as e:
                logging.error(f"Error syncing data for {stock.symbol}: {e}")
