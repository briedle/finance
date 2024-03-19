import requests
import pandas as pd
import time
import os
import copy

TOP_COMPANIES = [
    "AAPL",   # Apple Inc.
    "MSFT",   # Microsoft Corporation
    "AMZN",   # Amazon.com Inc.
    "GOOGL",  # Alphabet Inc. (Google)
    "META",   # Meta Platforms, Inc. (Facebook)
    "TSLA",   # Tesla, Inc.
    "BRK.A",  # Berkshire Hathaway Inc.
    "BRK.B",  # Berkshire Hathaway Inc.
    "NVDA",   # NVIDIA Corporation
    "JPM",    # JPMorgan Chase & Co.
    "JNJ",    # Johnson & Johnson
    "V",      # Visa Inc.
    "PG",     # Procter & Gamble Company
    "UNH",    # UnitedHealth Group Incorporated
    "MA",     # Mastercard Incorporated
    "PYPL",   # PayPal Holdings, Inc.
    "DIS",    # The Walt Disney Company
    "BABA",   # Alibaba Group Holding Limited
    "HD",     # The Home Depot, Inc.
    "CMCSA",  # Comcast Corporation
    "BAC",    # Bank of America Corporation
    "INTC",   # Intel Corporation
    "T",      # AT&T Inc.
    "KO",     # The Coca-Cola Company
    "WMT",    # Walmart Inc.
    "NFLX",   # Netflix, Inc.
    "PFE",    # Pfizer Inc.
    "ADBE",   # Adobe Inc.
    "CRM",    # salesforce.com, inc.
    "NKE",    # NIKE, Inc.
    "XOM",    # Exxon Mobil Corporation
    "MRK",    # Merck & Co., Inc.
    "CSCO",   # Cisco Systems, Inc.
    "ABT",    # Abbott Laboratories
    "TMO",    # Thermo Fisher Scientific Inc.
    "VZ",     # Verizon Communications Inc.
    "PEP",    # PepsiCo, Inc.
    "ORCL",   # Oracle Corporation
    "NVS",    # Novartis AG
    "ABBV",   # AbbVie Inc.
    "DHR",    # Danaher Corporation
    "BMY",    # Bristol Myers Squibb Co.
    "PM",     # Philip Morris International Inc.
    "LLY",    # Eli Lilly and Company
    "AVGO",   # Broadcom Inc.
    "GE",     # General Electric Company
    "CVX",    # Chevron Corporation
    "ABB",    # ABB Ltd.
    "DOW"     # Dow Inc.
]


def fetch_data(
    stock_symbol: str, 
    function: str, 
    api_key: None | str = None,
    **kwargs
):
    """
    Fetches data from the Alpha Vantage API for a given stock symbol and function.
    Will automatically retry if the request fails due to rate limiting.
    
    Parameters:
    - stock_symbol (str): The stock symbol to fetch data for.
    - function (str): The function to use for fetching data.
    - **kwargs: Additional parameters to pass to the API.
    
    Returns:
    - dict: The JSON response from the API.
    
    Raises:
        - ValueError: If the API request fails due to an invalid API key or
          unexpected response.
    """
    url = "https://alpha-vantage.p.rapidapi.com/query"
    
    querystring = {
        "symbol": stock_symbol,
        "function": function,
        "datatype": "json",
        **kwargs
    }
    
    if not api_key:
        api_key = os.getenv('RAPIDAPI_KEY')
        if not api_key:
            raise ValueError('API key not provided')
    
    headers = {
        "X-RapidAPI-Key": api_key,
        # "X-RapidAPI-Key": "1c63ffa51amsh98ddb79fb2729e8p14b4fajsn657b83e58886",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print('Rate limit exceeded.  Waiting 60 seconds and trying again.')
        time.sleep(60)
        return fetch_data(stock_symbol, function, api_key, **kwargs)
    else:
        error_message = f'Error fetching data: {response.status_code}'
        print(error_message)
        raise ValueError(error_message)

    
def pull_and_parse(
    companies: list[str], 
    fetch_function: str,
    parse_function,
    api_key: None | str = None,
):
    """
    Fetches and parses data for a list of companies.

    Args:
        companies (list[str]): A list of company names.
        fetch_function (str): The name of the function used to fetch data for a single company.
        parse_function: The function used to parse the fetched data.
        api_key (None | str, optional): An API key for accessing data. Defaults to None.

    Returns:
        tuple: A tuple containing two elements:
            - A pandas DataFrame containing the parsed data for all companies.
            - A list of companies that were not successfully parsed.

    """
    
    parsed_data = []
    companies_copy = copy.deepcopy(companies)
    
    for company in companies:
        parsed = single_pull_and_parse(
            company, 
            fetch_function, 
            parse_function,
            api_key=api_key
        )
        
        if parsed is not None:
            parsed_data.append(parsed)
            companies_copy.remove(company)
            print(f'{company} done and removed from list')
            
    return pd.concat(parsed_data), companies_copy


def single_pull_and_parse(
    company: str, 
    fetch_function: str,
    parse_function,
    api_key: None | str = None,
):
    """
    Fetches data for a given company using the specified fetch function,
    parses the data using the specified parse function, and returns the parsed data.
    
    Args:
        company (str): The name of the company to fetch data for.
        fetch_function (str): The name of the fetch function to use for fetching data.
        parse_function (function): The function to use for parsing the fetched data.
        api_key (str, optional): The API key to use for fetching data. Defaults to None.
    
    Returns:
        The parsed data obtained from the fetch and parse operations.
        Returns None if there was a problem during the fetch or parse operations.
    """
    try:
        data = fetch_data(
            company, 
            function=fetch_function,
            api_key=api_key
        )
        parsed_data = parse_function(data)
        return parsed_data
    except KeyError:
        print(f'{company} had a problem')
        return None
    



# STOCK PRICES AND VOLUMES
def parse_monthly_adjusted(data: dict) -> pd.DataFrame:
    """
    Create a dataframe from the given Alpha Vantage's TIME_SERIES_MONTHLY_ADJUSTED data.
    
    Args:
        data (dict): A dictionary containing the data for the dataframe.
        
    Returns:
        pd.DataFrame: The created dataframe.
    """
    stock_symbol = data['Meta Data']['2. Symbol']
    date_data = list(data['Monthly Adjusted Time Series'].keys())
    open_data = [data['Monthly Adjusted Time Series'][x]['1. open'] for x in date_data]
    high_data = [data['Monthly Adjusted Time Series'][x]['2. high'] for x in date_data]
    low_data = [data['Monthly Adjusted Time Series'][x]['3. low'] for x in date_data]
    close_data = [data['Monthly Adjusted Time Series'][x]['4. close'] for x in date_data]
    adj_close_data = [data['Monthly Adjusted Time Series'][x]['5. adjusted close'] for x in date_data]
    volume_data = [data['Monthly Adjusted Time Series'][x]['6. volume'] for x in date_data]
    dividend_data = [data['Monthly Adjusted Time Series'][x]['7. dividend amount'] for x in date_data]
    
    return pd.DataFrame({
        'symbol': stock_symbol,
        'date': date_data,
        'open': open_data,
        'high': high_data,
        'low': low_data,
        'close': close_data,
        'adj_close': adj_close_data,
        'volume': volume_data,
        'dividend': dividend_data
    })
    

# INCOME STATEMENT 

def parse_partial_income_statement(data, report_type: str):
    """
    Parses the income statement data and returns a dictionary containing various financial metrics.

    Args:
        data (dict): The income statement data.
        report_type (str): The type of report to parse. Must be either "annual" or "quarterly".

    Returns:
        dict: A dictionary containing the following financial metrics:
            - date_data: List of fiscal dates.
            - gross_profit: List of gross profit values.
            - total_revenue: List of total revenue values.
            - cost_of_revenue: List of cost of revenue values.
            - cogs: List of cost of goods and services sold values.
            - operating_income: List of operating income values.
            - net_investment_income: List of net investment income values.
            - net_interest_income: List of net interest income values.
            - interest_income: List of interest income values.
            - interest_expense: List of interest expense values.
            - non_interest_income: List of non-interest income values.
            - other_non_operating_income: List of other non-operating income values.
            - depreciation: List of depreciation values.
            - depreciation_amortization: List of depreciation and amortization values.
            - income_before_tax: List of income before tax values.
            - income_tax_expense: List of income tax expense values.
            - interest_and_debt_expense: List of interest and debt expense values.
            - net_income_from_continuing_operations: List of net income from continuing operations values.
            - comprensive_income: List of comprehensive income values.
            - ebit: List of EBIT (Earnings Before Interest and Taxes) values.
            - ebitda: List of EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) values.
            - net_income: List of net income values.

    Raises:
        ValueError: If the report_type is not "annual" or "quarterly".
    """
    
    if report_type == 'annual':
        report_data = data['annualReports']
    elif report_type == 'quarterly':
        report_data = data['quarterlyReports']
    else:
        raise ValueError('report_type must be either "annual" or "quarterly"')
    
    date = [x['fiscalDateEnding'] for x in report_data]
    gross_profit = [x['grossProfit'] for x in report_data]
    total_revenue = [x['totalRevenue'] for x in report_data]
    cost_of_revenue = [x['costOfRevenue'] for x in report_data]
    cogs = [x['costofGoodsAndServicesSold'] for x in report_data]
    operating_income = [x['operatingIncome'] for x in report_data]
    net_investment_income = [x['investmentIncomeNet'] for x in report_data]
    net_interest_income = [x['netInterestIncome'] for x in report_data]
    interest_income = [x['interestIncome'] for x in report_data]
    interest_expense = [x['interestExpense'] for x in report_data]
    non_interest_income = [x['nonInterestIncome'] for x in report_data]
    other_non_operating_income = [x['otherNonOperatingIncome'] for x in report_data]
    depreciation = [x['depreciation'] for x in report_data]
    depreciation_amortization = [x['depreciationAndAmortization'] for x in report_data]
    income_before_tax = [x['incomeBeforeTax'] for x in report_data]
    income_tax_expense = [x['incomeTaxExpense'] for x in report_data]
    interest_and_debt_expense = [x['interestAndDebtExpense'] for x in report_data]
    net_income_from_continuing_operations = [x['netIncomeFromContinuingOperations'] for x in report_data]
    comprehensive_income = [x['comprehensiveIncomeNetOfTax'] for x in report_data]
    ebit = [x['ebit'] for x in report_data]
    ebitda = [x['ebitda'] for x in report_data]
    net_income = [x['netIncome'] for x in report_data]
    
    result = pd.DataFrame({
        'symbol': data['symbol'],
        'report_type': report_type,
        'date': date,
        'gross_profit': gross_profit,
        'total_revenue': total_revenue,
        'cost_of_revenue': cost_of_revenue,
        'cogs': cogs,
        'operating_income': operating_income,
        'net_investment_income': net_investment_income,
        'net_interest_income': net_interest_income,
        'interest_income': interest_income,
        'interest_expense': interest_expense,
        'non_interest_income': non_interest_income,
        'other_non_operating_income': other_non_operating_income,
        'depreciation': depreciation,
        'depreciation_amortization': depreciation_amortization,
        'income_before_tax': income_before_tax,
        'income_tax_expense': income_tax_expense,
        'interest_and_debt_expense': interest_and_debt_expense,
        'net_income_from_continuing_operations': net_income_from_continuing_operations,
        'comprehensive_income': comprehensive_income,
        'ebit': ebit,
        'ebitda': ebitda,
        'net_income': net_income,
    })
    
    def str_none_to_none(value):
        if value in ['None', 'none', '']:
            return None
        else:
            return value


    for col in result.columns:
        if col in ('symbol', 'report_type'):
            result[col] = result[col].astype('str')
        elif col == 'date':
            result[col] = pd.to_datetime(result[col])
        else:
            result[col] = result[col].apply(str_none_to_none)
            result[col] = result[col].astype('float')
        
    return result
    
    
def parse_income_statement(data):
    annual = parse_partial_income_statement(data, 'annual')
    quarterly = parse_partial_income_statement(data, 'quarterly')
    return pd.concat([annual, quarterly])
  



if __name__ == '__main__':
    # Example usage
    data = fetch_data('AAPL')
    df = parse_monthly_adjusted(data)
    print(df.head())