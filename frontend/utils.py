from typing import List
import pandas as pd
from pytickersymbols import PyTickerSymbols
import os
from hints import get_stock_API, get_historical_prices


# Task 1
def transform_api_output(api_result: str):
    output = pd.DataFrame()
    # TODO: Transform result to pandas Dataframe

    return output

def get_stock_prices(stock: str, apikey: str):
    api_result = get_stock_API(stock, apikey)
    output = transform_api_output(api_result)
    output['ticker'] = stock
    output['close'] = output['close'].astype(float)
    return output

# Task 2
def get_or_load(stock: str, apikey: str, historical: bool = False):
    # Define folder, filename and file path
    if historical:
        data_dir = 'data/hist/'
    else:
        data_dir = 'data/current/'
    
    file_name = f'{stock}.csv'
    file_path = f'{data_dir}{file_name}'
    
    # Check if stock already in data lake
    if file_name in os.listdir(data_dir):
        data_stock = pd.read_csv(file_path)
        return data_stock
    
    # If stock not found locally, return API call
    if historical:
        data = get_historical_prices(stock, apikey)
    else:
        data = get_stock_prices(stock, apikey)
    if 'timestamp' in data.columns:
        data.to_csv(file_path)
    return data

# Task 3
def transform_hist_data(df: pd.DataFrame):
    output = df

    return output

def historical(stock: str, apikey: str):
    output = pd.DataFrame()
    current_data = get_or_load(stock, apikey)
    
    hist_data_raw = get_or_load(stock, apikey, historical=True)
    hist_data = transform_hist_data(hist_data_raw)
    
    output = pd.concat([current_data,hist_data])
    return output

# Task 4
def get_stocks(stocks: List[str], apikey: str):
    output = pd.DataFrame()
    # TODO: Expand the output to multiple stocks, use buffering function

    return pd.concat(output)


def get_ticker_symbols():
    stocks = ['AAPL', "IBM"]
    # TODO: Insert dataframe Transformation her

    return stocks

# Task 3
def get_performance(df: pd.DataFrame):
    return df



