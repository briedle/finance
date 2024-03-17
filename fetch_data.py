#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import pandas as pd
import numpy as np
import copy
import importlib

# import tkinter as tk
# import pyjsonviewer
# from pandas import json_normalize
# from flatten_json import flatten
import parse_alpha_vantage


importlib.reload(parse_alpha_vantage)


# In[4]:


top_companies = [
    "AAPL",   # Apple Inc.
    "MSFT",   # Microsoft Corporation
    "AMZN",   # Amazon.com Inc.
    "GOOGL",  # Alphabet Inc. (Google)
    "GOOG",   # Alphabet Inc. (Google)
    "META",     # Meta Platforms, Inc. (Facebook)
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


# In[5]:


parsed_data = []


# In[11]:





top_companies_copy = copy.deepcopy(top_companies)
for company in top_companies:
    try:
        data = parse_alpha_vantage.fetch_data(company)
        print(f'{company} data fetch succeeded')
        parsed_data.append(parse_alpha_vantage.parse_monthly_adjusted(data))
        print(f'{company} data parsing and appending succeeded')
        top_companies_copy.remove(company)
        print(f'{company} done and removed from list')
    except KeyError:
        print(f'{company} had problem')

top_companies = copy.deepcopy(top_companies_copy)



# In[25]:


company_prices = pd.concat(parsed_data)
company_prices = company_prices.drop_duplicates(['symbol', 'date'])
company_prices.to_csv('data/monthly_top50_company_prices.csv', index=False)

