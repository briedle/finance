import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_visualizer_backend.settings')
django.setup()

import requests  # noqa: E402
import bs4 as bs  # noqa: E402
import pandas as pd  # noqa: E402
import datetime  # noqa: E402
from stocks.models import BaseStockData  # noqa: E402


def pull_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    company_names = []
    sectors = []
    subindustries = []
    headquarters = []
    dates_added = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)
        company_name = row.findAll('td')[1].text
        company_names.append(company_name)
        sector = row.findAll('td')[2].text
        sectors.append(sector)
        subindustry = row.findAll('td')[3].text
        subindustries.append(subindustry)
        headquarter = row.findAll('td')[4].text
        headquarters.append(headquarter)
        date_added = row.findAll('td')[5].text
        dates_added.append(date_added)
    return pd.DataFrame({
        'symbol': tickers, 
        'name': company_names,
        'sector': sectors,
        'headquarters': headquarters,
        'date_added': [datetime.datetime.strptime(date.strip(), "%Y-%m-%d") for date in dates_added],
    })
    


if __name__ == '__main__':
    sp500_data = pull_sp500_tickers()
    
    # Prepare a list of BaseStockData instances
    stock_data_instances = [
        BaseStockData(
            symbol=row['symbol'],
            name=row['name'],
            sector=row['sector'],
            headquarters=row['headquarters'],
            date_added=row['date_added'],
        )
        for _, row in sp500_data.iterrows()
    ]

    # Bulk create instances
    BaseStockData.objects.bulk_create(stock_data_instances)