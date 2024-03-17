import requests
import pandas as pd
import time

def fetch_data(
    stock_symbol: str, 
    function: str = "TIME_SERIES_MONTHLY_ADJUSTED", 
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
    
    headers = {
        "X-RapidAPI-Key": "1c63ffa51amsh98ddb79fb2729e8p14b4fajsn657b83e58886",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print('Rate limit exceeded.  Waiting 60 seconds and trying again.')
        time.sleep(60)
        return fetch_data(stock_symbol, function, **kwargs)
    else:
        error_message = f'Error fetching data: {response.status_code}'
        print(error_message)
        raise ValueError(error_message)


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
    
# pyjsonviewer.view_data(json_data=response.json())