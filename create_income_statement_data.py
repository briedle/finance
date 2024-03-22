# import os
# import django

import os
from stocks.models import IncomeStatementData, BaseStockData
import pandas as pd
from django.db import IntegrityError

# Assuming you need to change the directory to read the CSV file
new_working_directory = "/home/briedle/web-projects/finance/stock_visualizer_backend"
try:
    os.chdir(new_working_directory)
    print("Changed the working directory to ", new_working_directory)
except FileNotFoundError:
    print("The directory does not exist: ", new_working_directory)
except PermissionError:
    print("You do not have permissions to change to the specified directory.")
    
print("Current working directory:", os.getcwd())

income_statement_data = pd.read_csv('../data/income_statement_data.csv')

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





# new_working_directory = "/home/briedle/web-projects/finance/stock_visualizer_backend"
# try:
#     os.chdir(new_working_directory)
#     print("Changed the working directory to ", new_working_directory)
# except FileNotFoundError:
#     print("The directory does not exist: ", new_working_directory)
# except PermissionError:
#     print("You do not have permissions to change to the specified directory.")
    
# print("Current working directory:", os.getcwd())

    
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_visualizer_backend.settings')
# django.setup()

# from stocks.models import IncomeStatementData, BaseStockData
# from asgiref.sync import sync_to_async
# from django.db import IntegrityError
# import pandas as pd

# # Wrap the synchronous Django ORM call
# get_stock_instance = sync_to_async(BaseStockData.objects.get, thread_sensitive=True)
# create_income_statement_instance = sync_to_async(IncomeStatementData.objects.create, thread_sensitive=True)

# income_statement_data = pd.read_csv('../data/income_statement_data.csv')
# # Assuming income_statement_data is your DataFrame
# for _, row in income_statement_data.iterrows():
#     # Fetch the corresponding BaseStockData instance
#     try:
#         # stock_instance = await get_stock_instance(symbol=row['symbol'])
#         stock_instance = BaseStockData.objects.get(symbol=row["symbol"])
#     except BaseStockData.DoesNotExist:
#         # Handle the case where the symbol does not exist
#         print(f"No BaseStockData found for symbol: {row['symbol']}")
#         continue
    
#         # Convert all 'nan' values in the row to None
#     for key, value in row.items():
#         if pd.isna(value):
#             row[key] = None

#     # Create and save the new IncomeStatementData instance
#     try:
#         # await create_income_statement_instance(
#         #     stock=stock_instance,
#         #     report_type=row["report_type"],
#         #     date=row["date"],
#         #     gross_profit=row["gross_profit"],
#         #     total_revenue=row["total_revenue"],
#         #     cost_of_revenue=row["cost_of_revenue"],
#         #     cogs=row["cogs"],
#         #     operating_income=row["operating_income"],
#         #     net_investment_income=row["net_investment_income"],
#         #     net_interest_income=row["net_interest_income"],
#         #     interest_income=row["interest_income"],
#         #     interest_expense=row["interest_expense"],
#         #     non_interest_income=row["non_interest_income"],
#         #     other_non_operating_income=row["other_non_operating_income"],
#         #     depreciation=row["depreciation"],
#         #     depreciation_amortization=row["depreciation_amortization"],
#         #     income_before_tax=row["income_before_tax"],
#         #     income_tax_expense=row["income_tax_expense"],
#         #     interest_and_debt_expense=row["interest_and_debt_expense"],
#         #     net_income_from_continuing_operations=row["net_income_from_continuing_operations"],
#         #     comprehensive_income=row["comprehensive_income"],
#         #     ebit=row["ebit"],
#         #     ebitda=row["ebitda"],
#         #     net_income=row["net_income"],
#         # )
#         IncomeStatementData.objects.create(
#             stock=stock_instance,
#             report_type=row["report_type"],
#             date=row["date"],
#             gross_profit=row["gross_profit"],
#             total_revenue=row["total_revenue"],
#             cost_of_revenue=row["cost_of_revenue"],
#             cogs=row["cogs"],
#             operating_income=row["operating_income"],
#             net_investment_income=row["net_investment_income"],
#             net_interest_income=row["net_interest_income"],
#             interest_income=row["interest_income"],
#             interest_expense=row["interest_expense"],
#             non_interest_income=row["non_interest_income"],
#             other_non_operating_income=row["other_non_operating_income"],
#             depreciation=row["depreciation"],
#             depreciation_amortization=row["depreciation_amortization"],
#             income_before_tax=row["income_before_tax"],
#             income_tax_expense=row["income_tax_expense"],
#             interest_and_debt_expense=row["interest_and_debt_expense"],
#             net_income_from_continuing_operations=row["net_income_from_continuing_operations"],
#             comprehensive_income=row["comprehensive_income"],
#             ebit=row["ebit"],
#             ebitda=row["ebitda"],
#             net_income=row["net_income"],
#         )
#     except IntegrityError as e:
#         print(e)
#         continue