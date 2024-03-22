from django.core.management.base import BaseCommand
from stocks.utils import parse_alpha_vantage as pav
from stocks.models import BaseStockData, MonthlyStockPriceData
from django.conf import settings
import logging


class Command(BaseCommand):
    help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

    function_to_syncing = {
        'TIME_SERIES_MONTHLY_ADJUSTED': pav.sync_monthly_adjusted,
        # Add other mappings as needed
    }

    function_to_model = {
        'TIME_SERIES_MONTHLY_ADJUSTED': MonthlyStockPriceData,
        # Add other mappings as needed
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

    def handle(self, *args, **options):
        function = options['function'].upper()
        start_index = options['start_index']
        stop_index = options['stop_index']
        check_exists = options['check_exists']

        # Apply slicing based on provided start and stop indices
        stocks_to_iterate = BaseStockData.objects.all()[start_index:stop_index]

        sync_func = self.function_to_syncing.get(function)
        model_class = self.function_to_model.get(function)  

        if not sync_func or not model_class:
            self.stdout.write(f"No syncing function or model found for {function}. Please check your mappings.")
            return

        for stock in stocks_to_iterate:
            if check_exists:
                # exists = model_class.objects.filter(stock=stock, function=function).exists()
                exists = model_class.objects.filter(stock=stock).exists()   
                if exists:
                    self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
                    continue

            try:
                data = pav.fetch_data(
                    stock.symbol,
                    function=function,
                    api_key=settings.RAPIDAPI_KEY
                )
                if data:
                    sync_func(data)
                    self.stdout.write(f"Fetched and synced data for {stock.symbol} using {sync_func.__name__}")
            except Exception as e:
                logging.error(f"Error fetching/syncing data for {stock.symbol}: {e}")

# class Command(BaseCommand):
#     help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

#     # Mapping from fetching functions to syncing functions
#     function_to_syncing = {
#         'TIME_SERIES_MONTHLY_ADJUSTED': pav.sync_monthly_adjusted,
#         # Add other mappings as needed
#     }

#     # Mapping from fetching functions to Django model classes
#     function_to_model = {
#         'TIME_SERIES_MONTHLY_ADJUSTED': MonthlyStockPriceData,
#         # Add other mappings as needed
#     }

#     def add_arguments(self, parser):
#         parser.add_argument('function', type=str, help='The function to fetch data for')
#         parser.add_argument(
#             '--no-check-exists',
#             action='store_false',
#             dest='check_exists', 
#             help='Do not check if the data already exists in the database'
#         )

#     def handle(self, *args, **options):
#         function = options['function']
#         check_exists = options['check_exists']
#         stocks_to_iterate = BaseStockData.objects.all()[10:50]

#         # Determine the syncing function and model for the given function
#         sync_func = self.function_to_syncing.get(function.upper())
#         model_class = self.function_to_model.get(function.upper())

#         if not sync_func or not model_class:
#             self.stdout.write(f"No syncing function or model found for {function}. Please check your mappings.")
#             return

#         for stock in stocks_to_iterate:
#             if check_exists:
#                 # Use the model class dynamically to check if data exists
#                 exists = model_class.objects.filter(stock=stock, function=function).exists()
#                 if exists:
#                     self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
#                     continue

#             data = pav.fetch_data(
#                 stock.symbol,
#                 function=function.upper(),
#                 api_key=settings.RAPIDAPI_KEY
#             )

#             # Call the syncing function
#             sync_func(data)
#             self.stdout.write(f"Fetched data for {stock.symbol} and synced using {sync_func.__name__}")



# class Command(BaseCommand):
#     help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

#     # Define a mapping of fetching functions to syncing functions
#     function_mapping = {
#         'TIME_SERIES_MONTHLY_ADJUSTED': pav.sync_monthly_adjusted,
#         # Add more mappings as needed
#     }

#     def add_arguments(self, parser):
#         parser.add_argument(
#             'function', 
#             type=str, 
#             choices=self.function_mapping.keys(), 
#             help='The function to fetch data for'
#         )
#         parser.add_argument(
#             '--no-check-exists',
#             action='store_false',
#             dest='check_exists', 
#             help='Do not check if the data already exists in the database'
#         )

#     def handle(self, *args, **options):
#         function = options['function']
#         check_exists = options['check_exists']
#         stocks_to_iterate = BaseStockData.objects.all()[10:50]

#         for stock in stocks_to_iterate:
#             if check_exists:
#                 exists = MonthlyStockPriceData.objects.filter(stock=stock).exists()
#                 if exists:
#                     self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
#                     continue

#             data = pav.fetch_data(
#                 stock.symbol,
#                 function=function.upper(),
#                 api_key=settings.RAPIDAPI_KEY
#             )

#             # Automatically determine and call the syncing function
#             syncing_function = self.function_mapping[function]
#             syncing_function(data)
#             self.stdout.write(f"Fetched and synced data for {stock.symbol} using {function}")


# class Command(BaseCommand):
#     help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

#     def add_arguments(self, parser):
#         parser.add_argument('fetch_function', type=str, help='The function to fetch data for')
#         parser.add_argument('sync_function', type=str, help='The sync function to use for updating the database')
#         parser.add_argument(
#             '--no-check-exists',
#             action='store_false',
#             dest='check_exists', 
#             help='Do not check if the data already exists in the database'
#         )

#     def handle(self, *args, **options):
#         fetch_function = options['fetch_function']
#         sync_function = options['sync_function']
#         check_exists = options['check_exists']

#         # Retrieve the syncing function dynamically
#         try:
#             syncing_function = getattr(pav, sync_function)
#         except AttributeError:
#             self.stdout.write(self.style.ERROR(f'Sync function "{sync_function}" not found in parse_alpha_vantage module.'))
#             return

#         stocks_to_iterate = BaseStockData.objects.all()[12:14]

#         for stock in stocks_to_iterate:
#             if check_exists:
#                 # Assume there's a way to determine if data exists based on function and stock
#                 exists = MonthlyStockPriceData.objects.filter(stock=stock).exists()
#                 if exists:
#                     self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
#                     continue

#             data = pav.fetch_data(
#                 stock.symbol,
#                 function=fetch_function.upper(),
#                 api_key=settings.RAPIDAPI_KEY
#             )

#             # Call the dynamic syncing function
#             syncing_function(data)
#             self.stdout.write(f"Fetched and synced data for {stock.symbol}")


# class Command(BaseCommand):
#     help = 'Fetches stock data for a set of stocks based on the provided function and checks for existing data if specified.'

#     def add_arguments(self, parser):
#         parser.add_argument('function', type=str, help='The function to fetch data for')
#         parser.add_argument(
#             '--no-check-exists',
#             action='store_false',
#             dest='check_exists', 
#             help='Do not check if the data already exists in the database'
#         )

#     def handle(self, *args, **options):
#         function = options['function']
#         check_exists = not options['no_check_exists']
#         stocks_to_iterate = BaseStockData.objects.all()[10:50]

#         for stock in stocks_to_iterate:
#             if check_exists:
#                 # Logic to check if data exists
#                 exists = MonthlyStockPriceData.objects.filter(stock=stock, function=function).exists()
#                 if exists:
#                     self.stdout.write(f"Data for {stock.symbol} already exists. Skipping API call.")
#                     continue

#             # If data doesn't exist, or check_exists is False, fetch the data
#             data = pav.fetch_data(
#                 stock.symbol,
#                 function=function.upper(),
#                 api_key=settings.RAPIDAPI_KEY
#             )

#             pav.sync_monthly_adjusted(data)
#             self.stdout.write(f"Fetched data for {stock.symbol}")