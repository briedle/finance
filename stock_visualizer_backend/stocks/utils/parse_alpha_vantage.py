import requests
import time
import datetime
from stocks.models import BaseStockData, MonthlyStockPriceData, IncomeStatementData, BalanceSheetData, EarningsData, CashFlowData, QuarterlyStockOverview, EarningsCalendarData
from django.conf import settings
import logging
from typing import Dict, Optional, Union, List
import re
import csv
from decimal import Decimal, InvalidOperation
from django.db import transaction


def safe_decimal(value: str, default: Optional[Decimal] = None) -> Optional[Decimal]:
    """
    Safely converts a string to a Decimal. If the conversion fails or the value is 'None',
    it returns a specified default value.

    Args:
        value (str): The string value to convert to Decimal.
        default (Optional[Decimal]): The default value to return in case of conversion failure.

    Returns:
        Optional[Decimal]: The converted Decimal value or the default value if conversion fails.
    """
    if value in (None, 'None', ''):
        return default
    try:
        return Decimal(value.strip())
    except (InvalidOperation, TypeError, ValueError):
        logging.error(f"Invalid decimal value: {value}")
        return default


def safe_int(value: str, default: Optional[int] = None) -> Optional[int]:
    """
    Safely converts a string to an integer. If the conversion fails or the value is 'None',
    it returns a specified default value.

    Args:
        value (str): The string value to convert to an integer.
        default (Optional[int]): The default value to return in case of conversion failure.

    Returns:
        Optional[int]: The converted integer value or the default value if conversion fails.
    """
    if value in (None, 'None', ''):
        return default
    try:
        return int(value.strip())
    except (ValueError, TypeError):
        logging.error(f"Invalid integer value: {value}")
        return default


def safe_date(value: str, default: Optional[datetime.date] = None) -> Optional[datetime.date]:
    """
    Safely converts a string to a date object. If the conversion fails or the value is 'None',
    it returns a specified default value.

    Args:
        value (str): The string value to convert to a datetime.date.
        default (Optional[datetime.date]): The default value to return in case of conversion failure.

    Returns:
        Optional[datetime.date]: The converted date object or the default value if conversion fails.
    """
    if value in (None, 'None', ''):
        return default
    try:
        return datetime.datetime.strptime(value.strip(), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        logging.error(f"Invalid date value: {value}")
        return default


def camel_to_snake(name: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Converts a string or a list of strings from camel case to snake case.
    
    This function handles consecutive capital letters and numbers, ensuring that
    sequences like 'HTTPError' or 'CamelW2WCase' are correctly converted to
    'http_error' and 'camel_w2w_case', respectively. It supports both single strings
    and lists of strings.

    Args:
        name (Union[str, List[str]]): A string or a list of strings in camel case to be converted.

    Returns:
        Union[str, List[str]]: The converted string or list of strings in snake case.

    Examples:
        camel_to_snake("CamelCase") returns "camel_case"
        camel_to_snake("CamelCamelCase") returns "camel_camel_case"
        camel_to_snake("CamelW2WCase") returns "camel_w2w_case"
        camel_to_snake(["CamelCase", "AnotherExample"]) returns ["camel_case", "another_example"]
        camel_to_snake("accumulatedDepreciationAmortizationPPE")
    """
    def convert(item: str) -> str:
        # Insert underscores before uppercase letters followed by lowercase letters
        item = re.sub(r'(?<!^)(?=(?:[A-Z][a-z]|(?<=[a-z0-9])[A-Z]|\d+[a-z]))', '_', item)
        # Handle special case for consecutive uppercase letters
        item = re.sub(r'(?<=[a-z])([A-Z]+)(?=[A-Z][a-z])', r'_\1', item)
        return item.lower()

    if isinstance(name, str):
        return convert(name)
    elif isinstance(name, list):
        return [convert(item) for item in name]
    else:
        raise TypeError("Input must be a string or a list of strings")



def fetch_data(
    function: str, 
    stock_symbol: None | str = None, 
    api_key: str = None,
    backoff_seconds: int = 60,
    max_retries: int = 5, 
    **kwargs
):
    """
    Fetches data from the Alpha Vantage API for a given stock symbol and function.
    Implements exponential backoff in case of rate limiting.

    Parameters:
    - function (str): The function to use for fetching data.
    - stock_symbol (optional - str): The stock symbol to fetch data for. For most functions, 
        this is required, but there are a few (e.g. LISTING_STATUS) where this is not a parameter.
    - api_key (str): The API key for Alpha Vantage.
    - max_retries (int): Maximum number of retries before giving up.
    - **kwargs: Additional parameters to pass to the API.

    Returns:
    - dict: The JSON response from the API.

    Raises:
    - ValueError: If the API request fails after the maximum number of retries.
    """
    url = "https://alpha-vantage.p.rapidapi.com/query"
    if stock_symbol:
        querystring = {"symbol": stock_symbol, "function": function, "datatype": "json", **kwargs}
    else:
        querystring = {"function": function, "datatype": "json", **kwargs}
    
    if not api_key:
        api_key = settings.RAPIDAPI_KEY
        # api_key = os.getenv("RAPIDAPI_KEY")
        if not api_key:
            raise ValueError('API key not provided')
    
    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"}

    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit exceeded
                print(f"Rate limit exceeded. Retrying in {backoff_seconds} seconds...")
                time.sleep(backoff_seconds)
                backoff_seconds *= 2  # Double the backoff time for the next retry
                retry_count += 1
            else:
                raise ValueError(f"Error fetching data: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(backoff_seconds)
            backoff_seconds *= 2
            retry_count += 1

    raise ValueError("Max retries exceeded. Failed to fetch data.")


def fetch_csv_data(
    function: str, 
    api_key: None | str = None, 
    backoff_seconds: int = 60, 
    max_retries: int = 5,
    **kwargs
) -> List[List[str]]:
    """
    Fetches CSV data from the Alpha Vantage API for a given function.
    Implements exponential backoff in case of rate limiting.

    Parameters:
    - function (str): The function to use for fetching data. Should be a function that 
        returns CSV data.
    - api_key (str, optional): The API key to use for fetching data. Defaults to None, in which
        case the API key from the settings file is used.
    - backoff_seconds (int): Initial backoff time in seconds in case of rate limiting.
    - max_retries (int): Maximum number of retries before giving up.
    - **kwargs: Additional parameters to pass to the API.

    Returns:
    - List[List[str]]: A list of rows from the CSV file, where each row is a list of strings.

    Raises:
    - ValueError: If the API request fails after the maximum number of retries.
    """
    
    if not api_key:
        api_key = settings.RAPIDAPI_KEY  # Or another way to fetch the API key
        if not api_key:
            raise ValueError('API key not provided')

    url = "https://www.alphavantage.co/query"
    params = {"function": function, "apikey": api_key, **kwargs}
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                decoded_content = response.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                return list(cr)
            elif response.status_code == 429:  # Rate limit exceeded
                print(f"Rate limit exceeded. Retrying in {backoff_seconds} seconds...")
                time.sleep(backoff_seconds)
                backoff_seconds *= 2  # Double the backoff time for the next retry
                retry_count += 1
            else:
                raise ValueError(f"Error fetching data: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(backoff_seconds)
            backoff_seconds *= 2
            retry_count += 1

    raise ValueError("Max retries exceeded. Failed to fetch data.")

def sync_monthly_adjusted(data: dict):
    """
    Parse the given Alpha Vantage's TIME_SERIES_MONTHLY_ADJUSTED data and create Django model 
    instances.

    Args:
        data (dict): A dictionary containing the data for parsing.
        ModelClass: The Django model class to instantiate with the parsed data.
    """
    stock_symbol = data['Meta Data']['2. Symbol']
    
    # Fetch the BaseStockData instance
    base_stock, _ = BaseStockData.objects.get_or_create(symbol=stock_symbol)
    
    for date_str, values in data['Monthly Adjusted Time Series'].items():
        date = safe_date(date_str)
        
        defaults = {
            'open': safe_decimal(values['1. open']),
            'high': safe_decimal(values['2. high']),
            'low': safe_decimal(values['3. low']),
            'close': safe_decimal(values['4. close']),
            'adj_close': safe_decimal(values['5. adjusted close']),
            'volume': safe_int(values['6. volume']),
            'dividend': safe_decimal(values['7. dividend amount']),
        }
        
        defaults = {key: value for key, value in defaults.items() if value is not None}
    
        MonthlyStockPriceData.objects.update_or_create(
            stock=base_stock,
            date=date,
            defaults=defaults
        )

# INCOME STATEMENT 

def sync_income_statement(data: Dict) -> None:
    """
    Parses the income statement data from Alpha Vantage and updates or creates corresponding 
    Django model instances.

    This function processes both annual and quarterly reports, updating the database with new
    or updated records for each entry. It logs errors and skips entries with non-USD currency
    or missing base stock data.

    Args:
        data (Dict): The income statement data from Alpha Vantage, including symbol, annual
        reports, and quarterly reports.
    """
    stock_symbol = data['symbol']
    
    try:
        base_stock = BaseStockData.objects.get(symbol=stock_symbol)
    except BaseStockData.DoesNotExist:
        logging.error(
            f"No BaseStockData found for stock symbol: {stock_symbol}. "
            f"Will not use this data."
        )
        return # Exit function if base stock data is not found
    
    for report_type, reports in [('annual', 'annualReports'), ('quarterly', 'quarterlyReports')]:
        for entry in data[reports]:
            if entry['reportedCurrency'] != 'USD':
                logging.error(
                    f"Reported currency is not USD for stock symbol: {stock_symbol}. "
                    f"Will not use this data."
                )
                return
            
            date=datetime.datetime.strptime(entry['fiscalDateEnding'], '%Y-%m-%d').date()
            defaults = {
                'gross_profit': safe_decimal(entry['grossProfit']),
                'total_revenue': safe_decimal(entry['totalRevenue']),
                'cost_of_revenue': safe_decimal(entry['costOfRevenue']),
                'cogs': safe_decimal(entry['costofGoodsAndServicesSold']),
                'operating_income': safe_decimal(entry['operatingIncome']),
                'net_investment_income': safe_decimal(entry['investmentIncomeNet']),
                'net_interest_income': safe_decimal(entry['netInterestIncome']),
                'interest_income': safe_decimal(entry['interestIncome']),
                'interest_expense': safe_decimal(entry['interestExpense']),
                'non_interest_income': safe_decimal(entry['nonInterestIncome']),
                'other_non_operating_income': safe_decimal(entry['otherNonOperatingIncome']),
                'depreciation': safe_decimal(entry['depreciation']),
                'depreciation_amortization': safe_decimal(entry['depreciationAndAmortization']),
                'income_before_tax': safe_decimal(entry['incomeBeforeTax']),
                'income_tax_expense': safe_decimal(entry['incomeTaxExpense']),
                'interest_and_debt_expense': safe_decimal(entry['interestAndDebtExpense']),
                'net_income_from_continuing_operations': safe_decimal(
                    entry['netIncomeFromContinuingOperations']
                ),
                'comprehensive_income': safe_decimal(entry['comprehensiveIncomeNetOfTax']),
                'ebit': safe_decimal(entry['ebit']),
                'ebitda': safe_decimal(entry['ebitda']),
                'net_income': safe_decimal(entry['netIncome']),
            }
            
            defaults = {key: value for key, value in defaults.items() if value is not None}
            
            IncomeStatementData.objects.update_or_create(
                stock=base_stock,
                report_type=report_type,
                date=date,
                defaults=defaults
            )
            
def sync_balance_sheet(data: Dict) -> None:
    """
    Parses the balance sheet data from Alpha Vantage and updates or creates corresponding 
    Django model instances.

    This function processes both annual and quarterly reports, updating the database with new
    or updated records for each entry. It logs errors and skips entries with non-USD currency
    or missing base stock data.

    Args:
        data (Dict): The balance sheet data from Alpha Vantage, including symbol, annual
        reports, and quarterly reports.
    """
    stock_symbol = data['symbol']
    
    try:
        base_stock = BaseStockData.objects.get(symbol=stock_symbol)
    except BaseStockData.DoesNotExist:
        logging.error(f"No BaseStockData found for stock symbol: {stock_symbol}. Will not use this data.")
        return  # Exit function if base stock data is not found
    
    for report_type, reports in [('annual', 'annualReports'), ('quarterly', 'quarterlyReports')]:
        for entry in data[reports]:
            if entry['reportedCurrency'] != 'USD':
                logging.error(f"Reported currency is not USD for stock symbol: {stock_symbol}. Will not use this data.")
                return
            
            date = datetime.datetime.strptime(entry['fiscalDateEnding'], '%Y-%m-%d').date()
            defaults = {
                # Replace these with actual mappings from your data source to the BalanceSheetData model
                'total_assets': safe_decimal(entry.get('totalAssets')),
                'total_current_assets': safe_decimal(entry.get('totalCurrentAssets')),
                'cash_and_cash_equivalents_at_carrying_value': safe_decimal(entry.get('cashAndCashEquivalentsAtCarryingValue')),
                'cash_and_short_term_investments': safe_decimal(entry.get('cashAndShortTermInvestments')),
                'inventory': safe_decimal(entry.get('inventory')),
                'current_net_receivables': safe_decimal(entry.get('currentNetReceivables')),
                'total_non_current_assets': safe_decimal(entry.get('totalNonCurrentAssets')),
                'property_plant_equipment': safe_decimal(entry.get('propertyPlantEquipment')),
                'accumulated_depreciation_amortization_ppe': safe_decimal(entry.get('accumulatedDepreciationAmortizationPPE')),
                'intangible_assets': safe_decimal(entry.get('intangibleAssets')),
                'intangible_assets_excluding_goodwill': safe_decimal(entry.get('intangibleAssetsExcludingGoodwill')),
                'goodwill': safe_decimal(entry.get('goodwill')),
                'investments': safe_decimal(entry.get('investments')),
                'long_term_investments': safe_decimal(entry.get('longTermInvestments')),
                'short_term_investments': safe_decimal(entry.get('shortTermInvestments')),
                'other_current_assets': safe_decimal(entry.get('otherCurrentAssets')),
                'other_non_current_assets': safe_decimal(entry.get('otherNonCurrentAssets')),
                'total_liabilities': safe_decimal(entry.get('totalLiabilities')),
                'total_current_liabilities': safe_decimal(entry.get('totalCurrentLiabilities')),
                'current_accounts_payable': safe_decimal(entry.get('currentAccountsPayable')),
                'deferred_revenue': safe_decimal(entry.get('deferredRevenue')),
                'current_debt': safe_decimal(entry.get('currentDebt')),
                'short_term_debt': safe_decimal(entry.get('shortTermDebt')),
                'total_non_current_liabilities': safe_decimal(entry.get('totalNonCurrentLiabilities')),
                'capital_lease_obligations': safe_decimal(entry.get('capitalLeaseObligations')),
                'long_term_debt': safe_decimal(entry.get('longTermDebt')),
                'current_long_term_debt': safe_decimal(entry.get('currentLongTermDebt')),
                'long_term_debt_noncurrent': safe_decimal(entry.get('longTermDebtNoncurrent')),
                'short_long_term_debt_total': safe_decimal(entry.get('shortLongTermDebtTotal')),
                'other_current_liabilities': safe_decimal(entry.get('otherCurrentLiabilities')),
                'other_non_current_liabilities': safe_decimal(entry.get('otherNonCurrentLiabilities')),
                'total_shareholder_equity': safe_decimal(entry.get('totalShareholderEquity')),
                'treasury_stock': safe_decimal(entry.get('treasuryStock')),
                'retained_earnings': safe_decimal(entry.get('retainedEarnings')),
                'common_stock': safe_decimal(entry.get('commonStock')),
                'common_stock_shares_outstanding': safe_decimal(entry.get('commonStockSharesOutstanding')),
            }
            
            defaults = {key: value for key, value in defaults.items() if value is not None}
            
            BalanceSheetData.objects.update_or_create(
                stock=base_stock,
                report_type=report_type,
                date=date,
                defaults=defaults
            )


def sync_cash_flow(data: Dict) -> None:
    """
    Parses the cash flow data from Alpha Vantage and updates or creates corresponding 
    Django model instances.

    This function processes both annual and quarterly reports, updating the database with new
    or updated records for each entry. It logs errors and skips entries with non-USD currency
    or missing base stock data.

    Args:
        data (Dict): The cash flow data from Alpha Vantage, including symbol, annual
        reports, and quarterly reports.
    """
    stock_symbol = data['symbol']
    
    try:
        base_stock = BaseStockData.objects.get(symbol=stock_symbol)
    except BaseStockData.DoesNotExist:
        logging.error(f"No BaseStockData found for stock symbol: {stock_symbol}. Will not use this data.")
        return
    
    for report_type, reports in [('annual', 'annualReports'), ('quarterly', 'quarterlyReports')]:
        for entry in data[reports]:
            if entry['reportedCurrency'] != 'USD':
                logging.error(f"Reported currency is not USD for stock symbol: {stock_symbol}. Will not use this data.")
                return
            
            date = datetime.datetime.strptime(entry['fiscalDateEnding'], '%Y-%m-%d').date()
            defaults = {
                'operating_cashflow': safe_decimal(entry.get('operatingCashflow')),
                'payments_for_operating_activities': safe_decimal(entry.get('paymentsForOperatingActivities')),
                'proceeds_from_operating_activities': safe_decimal(entry.get('proceedsFromOperatingActivities')),
                'change_in_operating_liabilities': safe_decimal(entry.get('changeInOperatingLiabilities')),
                'change_in_operating_assets': safe_decimal(entry.get('changeInOperatingAssets')),
                'depreciation_depletion_and_amortization': safe_decimal(entry.get('depreciationDepletionAndAmortization')),
                'capital_expenditures': safe_decimal(entry.get('capitalExpenditures')),
                'change_in_receivables': safe_decimal(entry.get('changeInReceivables')),
                'change_in_inventory': safe_decimal(entry.get('changeInInventory')),
                'profit_loss': safe_decimal(entry.get('profitLoss')),
                'cashflow_from_investment': safe_decimal(entry.get('cashflowFromInvestment')),
                'cashflow_from_financing': safe_decimal(entry.get('cashflowFromFinancing')),
                'proceeds_from_repayments_of_short_term_debt': safe_decimal(entry.get('proceedsFromRepaymentsOfShortTermDebt')),
                'payments_for_repurchase_of_common_stock': safe_decimal(entry.get('paymentsForRepurchaseOfCommonStock')),
                'payments_for_repurchase_of_equity': safe_decimal(entry.get('paymentsForRepurchaseOfEquity')),
                'payments_for_repurchase_of_preferred_stock': safe_decimal(entry.get('paymentsForRepurchaseOfPreferredStock')),
                'dividend_payout': safe_decimal(entry.get('dividendPayout')),
                'dividend_payout_common_stock': safe_decimal(entry.get('dividendPayoutCommonStock')),
                'dividend_payout_preferred_stock': safe_decimal(entry.get('dividendPayoutPreferredStock')),
                'proceeds_from_issuance_of_common_stock': safe_decimal(entry.get('proceedsFromIssuanceOfCommonStock')),
                'proceeds_issuance_long_term_debt_capital_sec_net': safe_decimal(entry.get('proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet')),
                'proceeds_from_issuance_of_preferred_stock': safe_decimal(entry.get('proceedsFromIssuanceOfPreferredStock')),
                'proceeds_from_repurchase_of_equity': safe_decimal(entry.get('proceedsFromRepurchaseOfEquity')),
                'proceeds_from_sale_of_treasury_stock': safe_decimal(entry.get('proceedsFromSaleOfTreasuryStock')),
                'change_in_cash_and_cash_equivalents': safe_decimal(entry.get('changeInCashAndCashEquivalents')),
                'change_in_exchange_rate': safe_decimal(entry.get('changeInExchangeRate')),
                'net_income': safe_decimal(entry.get('netIncome')),
            }     
            defaults = {k: v for k, v in defaults.items() if v is not None}
            
            CashFlowData.objects.update_or_create(
                stock=base_stock,
                report_type=report_type,
                date=date,
                defaults=defaults
            )


def sync_earnings(data: Dict) -> None:
    """
    Parses the earnings data from Alpha Vantage and updates or creates corresponding 
    Django model instances for EarningsData.

    This function processes both annual and quarterly earnings, updating the database with new
    or updated records for each entry. It logs errors and skips entries without necessary data.

    Args:
        data (Dict): The earnings data from Alpha Vantage, including symbol, annual
        earnings, and quarterly earnings.
    """
    stock_symbol = data['symbol']

    try:
        base_stock = BaseStockData.objects.get(symbol=stock_symbol)
    except BaseStockData.DoesNotExist:
        logging.error(f"No BaseStockData found for stock symbol: {stock_symbol}. Will not use this data.")
        return

    # Process annual earnings
    for annual_earning in data.get('annualEarnings', []):
        date = datetime.datetime.strptime(annual_earning['fiscalDateEnding'], '%Y-%m-%d').date()
        defaults = {
            'reported_eps': safe_decimal(annual_earning.get('reportedEPS')),
        }

        EarningsData.objects.update_or_create(
            stock=base_stock,
            report_type='annual',
            date=date,
            defaults=defaults
        )

    # Process quarterly earnings
    for quarterly_earning in data.get('quarterlyEarnings', []):
        date = datetime.datetime.strptime(quarterly_earning['fiscalDateEnding'], '%Y-%m-%d').date()
        defaults = {
            'reported_eps': safe_decimal(quarterly_earning.get('reportedEPS')),
            'estimated_eps': safe_decimal(quarterly_earning.get('estimatedEPS')),
            'surprise': safe_decimal(quarterly_earning.get('surprise')),
            'surprise_percentage': safe_decimal(quarterly_earning.get('surprisePercentage')),
        }

        EarningsData.objects.update_or_create(
            stock=base_stock,
            report_type='quarterly',
            date=date,
            defaults=defaults
        )




def sync_base_and_quarterly_overview(data: Dict) -> None:
    """
    Parses the company data from Alpha Vantage and updates or creates corresponding 
    Django model instances for BaseStockData and QuarterlyStockOverview.
    
    This is the parsing function for the 'OVERVIEW' function from Alpha Vantage.

    Args:
        data (Dict): The company data from Alpha Vantage, including symbol, company information,
        and quarterly reports.
    """
    # Extract and update base stock data
    stock_symbol = data['Symbol']
    base_stock_defaults = {
        'name': data.get('Name'),
        'description': data.get('Description'),
        'headquarters': data.get('Address'),
        'cik': data.get('CIK'),
        'exchange': data.get('Exchange'),
        'country': data.get('Country'),
        'currency': data.get('Currency'),
        'sector': data.get('Sector'),
        'industry': data.get('Industry'),
        'fiscal_year_end': data.get('FiscalYearEnd'),
    }
    
    base_stock_defaults = {key: value for key, value in base_stock_defaults.items() if value is not None}
    
    base_stock, _ = BaseStockData.objects.update_or_create(
        symbol=stock_symbol, defaults=base_stock_defaults
    )

    quarter_end_date = datetime.datetime.strptime(data['LatestQuarter'], '%Y-%m-%d').date()
    overview_defaults = {
        'market_capitalization': safe_decimal(data.get('MarketCapitalization')),
        'ebitda': safe_decimal(data.get('EBITDA')),
        'pe_ratio': safe_decimal(data.get('PERatio')),
        'peg_ratio': safe_decimal(data.get('PEGRatio')),
        'book_value': safe_decimal(data.get('BookValue')),
        'dividend_per_share': safe_decimal(data.get('DividendPerShare')),
        'dividend_yield': safe_decimal(data.get('DividendYield')),
        'eps': safe_decimal(data.get('EPS')),
        'revenue_per_share_ttm': safe_decimal(data.get('RevenuePerShareTTM')),
        'profit_margin': safe_decimal(data.get('ProfitMargin')),
        'operating_margin_ttm': safe_decimal(data.get('OperatingMarginTTM')),
        'return_on_assets_ttm': safe_decimal(data.get('ReturnOnAssetsTTM')),
        'return_on_equity_ttm': safe_decimal(data.get('ReturnOnEquityTTM')),
        'revenue_ttm': safe_decimal(data.get('RevenueTTM')),
        'gross_profit_ttm': safe_decimal(data.get('GrossProfitTTM')),
        'diluted_eps_ttm': safe_decimal(data.get('DilutedEPSTTM')),
        'quarterly_earnings_growth_yoy': safe_decimal(data.get('QuarterlyEarningsGrowthYOY')),
        'quarterly_revenue_growth_yoy': safe_decimal(data.get('QuarterlyRevenueGrowthYOY')),
        'analyst_target_price': safe_decimal(data.get('AnalystTargetPrice')),
        'analyst_rating_strong_buy': safe_int(data.get('AnalystRatingStrongBuy')),
        'analyst_rating_buy': safe_int(data.get('AnalystRatingBuy')),
        'analyst_rating_hold': safe_int(data.get('AnalystRatingHold')),
        'analyst_rating_sell': safe_int(data.get('AnalystRatingSell')),
        'analyst_rating_strong_sell': safe_int(data.get('AnalystRatingStrongSell')),
        'trailing_pe': safe_decimal(data.get('TrailingPE')),
        'forward_pe': safe_decimal(data.get('ForwardPE')),
        'price_to_sales_ratio_ttm': safe_decimal(data.get('PriceToSalesRatioTTM')),
        'price_to_book_ratio': safe_decimal(data.get('PriceToBookRatio')),
        'ev_to_revenue': safe_decimal(data.get('EVToRevenue')),
        'ev_to_ebitda': safe_decimal(data.get('EVToEBITDA')),
        'beta': safe_decimal(data.get('Beta')),
        'week_high_52': safe_decimal(data.get('52WeekHigh')),
        'week_low_52': safe_decimal(data.get('52WeekLow')),
        'day_moving_average_50': safe_decimal(data.get('50DayMovingAverage')),
        'day_moving_average_200': safe_decimal(data.get('200DayMovingAverage')),
        'shares_outstanding': safe_decimal(data.get('SharesOutstanding')),
        'dividend_date': safe_date(data.get('DividendDate')),
        'ex_dividend_date': safe_date(data.get('ExDividendDate')),
    }
    overview_defaults = {key: value for key, value in overview_defaults.items() if value is not None}

    # Using get_or_create to avoid creating duplicates
    QuarterlyStockOverview.objects.update_or_create(
        stock=base_stock,
        quarter_end_date=quarter_end_date,
        defaults=overview_defaults
    )
    
    
def sync_earnings_calendar(api_key: str = 'demo', horizon: str = '3month'):
    """
    Syncs the earnings calendar data from the Alpha Vantage API.
    
    This function is quite different from the other syncing functions in that:
      1.  It does not use a stock_symbol -- it returns a giant amount of data 
      2.  It returns a csv, not json
      3.  We are not going to run this through the sync_av_data command line tool.  We are just 
          going to execute this from the Django shell.
      4.  We 

    Args:
        api_key (str): The API key for Alpha Vantage.
        horizon (str): The horizon parameter for the API call, e.g., "3month".
    """
    CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon={horizon}&apikey={api_key}'
    current_date = datetime.date.today()

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        next(cr)  # Skip header row

        with transaction.atomic():
            for row in cr:
                symbol, name, report_date, fiscal_date_ending, estimate, currency = row

                # Skip rows where the estimate is missing
                if not estimate:
                    continue

                # Create or update BaseStockData only if estimate is present
                stock, _ = BaseStockData.objects.get_or_create(
                    symbol=symbol,
                    defaults={'name': name, 'currency': currency}
                )

                # Create or update EarningsCalendarData
                horizon_months = int(horizon.replace('month', ''))
                estimate_decimal = safe_decimal(estimate)
                EarningsCalendarData.objects.update_or_create(
                    stock=stock,
                    current_date=current_date,
                    report_date=datetime.datetime.strptime(report_date, '%Y-%m-%d').date(),
                    defaults={
                        'horizon_months': horizon_months,
                        'fiscal_date_ending': datetime.datetime.strptime(fiscal_date_ending, '%Y-%m-%d').date(),
                        'estimate': estimate_decimal,
                    }
                )



# def fetch_data(
#     stock_symbol: str, 
#     function: str, 
#     api_key: None | str = None,
#     **kwargs
# ):
#     """
#     Fetches data from the Alpha Vantage API for a given stock symbol and function.
#     Will automatically retry if the request fails due to rate limiting.
    
#     Parameters:
#     - stock_symbol (str): The stock symbol to fetch data for.
#     - function (str): The function to use for fetching data.
#     - **kwargs: Additional parameters to pass to the API.
    
#     Returns:
#     - dict: The JSON response from the API.
    
#     Raises:
#         - ValueError: If the API request fails due to an invalid API key or
#           unexpected response.
#     """
#     url = "https://alpha-vantage.p.rapidapi.com/query"
    
#     querystring = {
#         "symbol": stock_symbol,
#         "function": function,
#         "datatype": "json",
#         **kwargs
#     }
    
#     if not api_key:
#         api_key = settings.RAPIDAPI_KEY
#         # api_key = os.getenv("RAPIDAPI_KEY")
#         if not api_key:
#             raise ValueError('API key not provided')
    
#     headers = {
#         "X-RapidAPI-Key": api_key,
#         "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
#     }
    
#     response = requests.get(url, headers=headers, params=querystring)
    
#     if response.status_code == 200:
#         return response.json()
#     elif response.status_code == 429:
#         print('Rate limit exceeded.  Waiting 60 seconds and trying again.')
#         time.sleep(60)
#         return fetch_data(stock_symbol, function, api_key, **kwargs)
#     else:
#         error_message = f'Error fetching data: {response.status_code}'
#         print(error_message)
#         raise ValueError(error_message)

# def pull_and_parse(
#     companies: list[str], 
#     fetch_function: str,
#     parse_function,
#     api_key: None | str = None,
# ):
#     """
#     Fetches and parses data for a list of companies.

#     Args:
#         companies (list[str]): A list of company names.
#         fetch_function (str): The name of the Alpha Vantage function used to fetch data for a single company.
#         parse_function: The function used to parse the fetched data.
#         api_key (None | str, optional): An API key for accessing data. Defaults to None.

#     Returns:
#         tuple: A tuple containing two elements:
#             - A pandas DataFrame containing the parsed data for all companies.
#             - A list of companies that were not successfully parsed.

#     """
    
#     parsed_data = []
#     companies_copy = copy.deepcopy(companies)
    
#     for company in companies:
#         parsed = single_pull_and_parse(
#             company, 
#             fetch_function, 
#             parse_function,
#             api_key=api_key
#         )
        
#         if parsed is not None:
#             parsed_data.append(parsed)
#             companies_copy.remove(company)
#             print(f'{company} done and removed from list')
            
#     return pd.concat(parsed_data, ignore_index=True), companies_copy


# def single_pull_and_parse(
#     company: str, 
#     fetch_function: str,
#     parse_function,
#     api_key: None | str = None,
# ):
#     """
#     Fetches data for a given company using the specified fetch function,
#     parses the data using the specified parse function, and returns the parsed data.
    
#     Args:
#         company (str): The name of the company to fetch data for.
#         fetch_function (str): The name of the fetch function to use for fetching data.
#         parse_function (function): The function to use for parsing the fetched data.
#         api_key (str, optional): The API key to use for fetching data. Defaults to None.
    
#     Returns:
#         The parsed data obtained from the fetch and parse operations.
#         Returns None if there was a problem during the fetch or parse operations.
#     """
#     try:
#         data = fetch_data(
#             company, 
#             function=fetch_function,
#             api_key=api_key
#         )
#         parsed_data = parse_function(data)
#         return parsed_data
#     except KeyError:
#         print(f'{company} had a problem')
#         return None



# STOCK PRICES AND VOLUMES
# def parse_monthly_adjusted(data: dict) -> pd.DataFrame:
#     """
#     Create a dataframe from the given Alpha Vantage's TIME_SERIES_MONTHLY_ADJUSTED data.
    
#     Args:
#         data (dict): A dictionary containing the data for the dataframe.
        
#     Returns:
#         pd.DataFrame: The created dataframe.
#     """
#     stock_symbol = data['Meta Data']['2. Symbol']
#     date_data = list(data['Monthly Adjusted Time Series'].keys())
#     open_data = [data['Monthly Adjusted Time Series'][x]['1. open'] for x in date_data]
#     high_data = [data['Monthly Adjusted Time Series'][x]['2. high'] for x in date_data]
#     low_data = [data['Monthly Adjusted Time Series'][x]['3. low'] for x in date_data]
#     close_data = [data['Monthly Adjusted Time Series'][x]['4. close'] for x in date_data]
#     adj_close_data = [data['Monthly Adjusted Time Series'][x]['5. adjusted close'] for x in date_data]
#     volume_data = [data['Monthly Adjusted Time Series'][x]['6. volume'] for x in date_data]
#     dividend_data = [data['Monthly Adjusted Time Series'][x]['7. dividend amount'] for x in date_data]
    
#     return pd.DataFrame({
#         'symbol': stock_symbol,
#         'date': date_data,
#         'open': open_data,
#         'high': high_data,
#         'low': low_data,
#         'close': close_data,
#         'adj_close': adj_close_data,
#         'volume': volume_data,
#         'dividend': dividend_data
#     })








# def sync_income_statement(data: Dict) -> None:
#     """
#     Parses the income statement data from Alpha Vantage and updates or creates corresponding Django model instances.

#     This function processes both annual and quarterly reports, updating the database with new or updated records
#     for each entry. It logs errors and skips entries with non-USD currency or missing base stock data.

#     Args:
#         data (Dict): The income statement data from Alpha Vantage, including symbol, annual reports, and quarterly reports.
#     """
#     stock_symbol = data['symbol']

#     # Fetch the BaseStockData instance or log error if not found
#     try:
#         base_stock, _ = BaseStockData.objects.get_or_create(symbol=stock_symbol)
#     except BaseStockData.DoesNotExist:
#         logging.error(f"No BaseStockData found for stock symbol: {stock_symbol}. Will not process this data.")
#         return  # Exit function if base stock data is not found

#     # Process each report type
#     for report_type, reports in [('annual', 'annualReports'), ('quarterly', 'quarterlyReports')]:
#         for entry in data[reports]:
#             if entry['reportedCurrency'] != 'USD':
#                 logging.error(f"Reported currency is not USD for stock symbol: {stock_symbol} in {report_type} report. Skipping this entry.")
#                 continue

#             date = datetime.datetime.strptime(entry['fiscalDateEnding'], '%Y-%m-%d').date()
#             defaults = {key: decimal.Decimal(value) for key, value in entry.items() if key != 'reportedCurrency' and key != 'fiscalDateEnding'}

#             IncomeStatementData.objects.update_or_create(
#                 stock=base_stock,
#                 report_type=report_type,
#                 date=date,
#                 defaults=defaults
#             )
        
# def parse_partial_income_statement(data, report_type: str):
#     """
#     Parses the income statement data and returns a dictionary containing various financial metrics.

#     Args:
#         data (dict): The income statement data.
#         report_type (str): The type of report to parse. Must be either "annual" or "quarterly".

#     Returns:
#         dict: A dictionary containing the following financial metrics:
#             - date_data: List of fiscal dates.
#             - gross_profit: List of gross profit values.
#             - total_revenue: List of total revenue values.
#             - cost_of_revenue: List of cost of revenue values.
#             - cogs: List of cost of goods and services sold values.
#             - operating_income: List of operating income values.
#             - net_investment_income: List of net investment income values.
#             - net_interest_income: List of net interest income values.
#             - interest_income: List of interest income values.
#             - interest_expense: List of interest expense values.
#             - non_interest_income: List of non-interest income values.
#             - other_non_operating_income: List of other non-operating income values.
#             - depreciation: List of depreciation values.
#             - depreciation_amortization: List of depreciation and amortization values.
#             - income_before_tax: List of income before tax values.
#             - income_tax_expense: List of income tax expense values.
#             - interest_and_debt_expense: List of interest and debt expense values.
#             - net_income_from_continuing_operations: List of net income from continuing operations values.
#             - comprensive_income: List of comprehensive income values.
#             - ebit: List of EBIT (Earnings Before Interest and Taxes) values.
#             - ebitda: List of EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) values.
#             - net_income: List of net income values.

#     Raises:
#         ValueError: If the report_type is not "annual" or "quarterly".
#     """
    
#     if report_type == 'annual':
#         report_data = data['annualReports']
#     elif report_type == 'quarterly':
#         report_data = data['quarterlyReports']
#     else:
#         raise ValueError('report_type must be either "annual" or "quarterly"')
    
    # date = [x['fiscalDateEnding'] for x in report_data]
    # gross_profit = [x['grossProfit'] for x in report_data]
    # total_revenue = [x['totalRevenue'] for x in report_data]
    # cost_of_revenue = [x['costOfRevenue'] for x in report_data]
    # cogs = [x['costofGoodsAndServicesSold'] for x in report_data]
    # operating_income = [x['operatingIncome'] for x in report_data]
    # net_investment_income = [x['investmentIncomeNet'] for x in report_data]
    # net_interest_income = [x['netInterestIncome'] for x in report_data]
    # interest_income = [x['interestIncome'] for x in report_data]
    # interest_expense = [x['interestExpense'] for x in report_data]
    # non_interest_income = [x['nonInterestIncome'] for x in report_data]
    # other_non_operating_income = [x['otherNonOperatingIncome'] for x in report_data]
    # depreciation = [x['depreciation'] for x in report_data]
    # depreciation_amortization = [x['depreciationAndAmortization'] for x in report_data]
    # income_before_tax = [x['incomeBeforeTax'] for x in report_data]
    # income_tax_expense = [x['incomeTaxExpense'] for x in report_data]
    # interest_and_debt_expense = [x['interestAndDebtExpense'] for x in report_data]
    # net_income_from_continuing_operations = [x['netIncomeFromContinuingOperations'] for x in report_data]
    # comprehensive_income = [x['comprehensiveIncomeNetOfTax'] for x in report_data]
    # ebit = [x['ebit'] for x in report_data]
    # ebitda = [x['ebitda'] for x in report_data]
    # net_income = [x['netIncome'] for x in report_data]
    
#     result = pd.DataFrame({
#         'symbol': data['symbol'],
#         'report_type': report_type,
#         'date': date,
#         'gross_profit': gross_profit,
#         'total_revenue': total_revenue,
#         'cost_of_revenue': cost_of_revenue,
#         'cogs': cogs,
#         'operating_income': operating_income,
#         'net_investment_income': net_investment_income,
#         'net_interest_income': net_interest_income,
#         'interest_income': interest_income,
#         'interest_expense': interest_expense,
#         'non_interest_income': non_interest_income,
#         'other_non_operating_income': other_non_operating_income,
#         'depreciation': depreciation,
#         'depreciation_amortization': depreciation_amortization,
#         'income_before_tax': income_before_tax,
#         'income_tax_expense': income_tax_expense,
#         'interest_and_debt_expense': interest_and_debt_expense,
#         'net_income_from_continuing_operations': net_income_from_continuing_operations,
#         'comprehensive_income': comprehensive_income,
#         'ebit': ebit,
#         'ebitda': ebitda,
#         'net_income': net_income,
#     })
    

#     for col in result.columns:
#         if col in ('symbol', 'report_type'):
#             result[col] = result[col].astype('str')
#         elif col == 'date':
#             result[col] = pd.to_datetime(result[col])
#         else:
#             result[col] = result[col].apply(str_none_to_none)
#             result[col] = result[col].astype('float')
        
#     return result
    
    
# def parse_income_statement(data):
#     annual = parse_partial_income_statement(data, 'annual')
#     quarterly = parse_partial_income_statement(data, 'quarterly')
#     return pd.concat([annual, quarterly])
  
def str_none_to_none(value):
    if value in ['None', 'none', '']:
        return None
    else:
        return value


if __name__ == '__main__':
    # Example usage
    data = fetch_data('AAPL')
    df = sync_monthly_adjusted(data)
    print(df.head())