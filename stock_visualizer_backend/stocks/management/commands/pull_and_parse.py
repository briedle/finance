# myapp/management/commands/fetch_stock_data.py
from django.core.management.base import BaseCommand
from django.apps import apps
import pandas as pd
import os
import sys

# Adjust the import path based on your project structure
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_directory = os.path.dirname(project_directory)
sys.path.append(parent_directory)

# Import the utility module
import parse_alpha_vantage as pav

class Command(BaseCommand):
    help = 'Fetches stock data from Alpha Vantage and stores it in the database'

    def add_arguments(self, parser):
        parser.add_argument('companies', nargs='+', type=str, help='List of company symbols')
        parser.add_argument('fetch_function', type=str, help='Alpha Vantage API function to use')
        parser.add_argument('parse_function', type=str, help='Function to parse the API response')
        parser.add_argument('model', type=str, help='Django model to use for storing data')
        parser.add_argument('--api_key', type=str, help='API key for Alpha Vantage')

    def handle(self, *args, **options):
        companies = options['companies']
        fetch_function = options['fetch_function']
        parse_function_name = options['parse_function']
        model_name = options['model']
        api_key = options.get('api_key')

        # Dynamically get the parse function from the pav module
        parse_function = getattr(pav, parse_function_name)

        # Dynamically get the model class
        ModelClass = apps.get_model('your_app_name', model_name)

        # Fetch and parse the data
        df, _ = pav.pull_and_parse(companies, fetch_function, parse_function, api_key)

        # Store the data in the Django database using the specified model
        for _, row in df.iterrows():
            ModelClass.objects.update_or_create(
                record_date=row['record_date'],
                defaults=row.to_dict()
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored stock data using {model_name}'))
