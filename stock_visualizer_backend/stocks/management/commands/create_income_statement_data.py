from django.core.management.base import BaseCommand
from stocks.models import IncomeStatementData, BaseStockData
import pandas as pd
from django.db import IntegrityError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Imports preprocessed income statement data'
    
    def add_arguments(self, parser):
         # Define a new command-line argument
        parser.add_argument(
            '--file_name', 
            type=str, 
            default='income_statement_data.csv',
            help='The filename of the CSV containing the income statement data.'
        )
    
    def handle(self, *args, **kwargs):  
        # Use the provided filename argument
        file_name = kwargs['file_name']
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'data', file_name)
        income_statement_data = pd.read_csv(file_path)
        
        for _, row in income_statement_data.iterrows():
            try:
                stock_instance = BaseStockData.objects.get(symbol=row["symbol"])
            except BaseStockData.DoesNotExist:
                print(f"No BaseStockData found for symbol: {row['symbol']}")
                continue

            for key, value in row.items():
                if pd.isna(value):
                    row[key] = None

            try:
                IncomeStatementData.objects.create(
                    stock=stock_instance,
                    report_type=row["report_type"],
                    date=row["date"],
                    gross_profit=row["gross_profit"],
                    total_revenue=row["total_revenue"],
                    cost_of_revenue=row["cost_of_revenue"],
                    cogs=row["cogs"],
                    operating_income=row["operating_income"],
                    net_investment_income=row["net_investment_income"],
                    net_interest_income=row["net_interest_income"],
                    interest_income=row["interest_income"],
                    interest_expense=row["interest_expense"],
                    non_interest_income=row["non_interest_income"],
                    other_non_operating_income=row["other_non_operating_income"],
                    depreciation=row["depreciation"],
                    depreciation_amortization=row["depreciation_amortization"],
                    income_before_tax=row["income_before_tax"],
                    income_tax_expense=row["income_tax_expense"],
                    interest_and_debt_expense=row["interest_and_debt_expense"],
                    net_income_from_continuing_operations=row["net_income_from_continuing_operations"],
                    comprehensive_income=row["comprehensive_income"],
                    ebit=row["ebit"],
                    ebitda=row["ebitda"],
                    net_income=row["net_income"],
                )
            except IntegrityError as e:
                print(e)
                continue