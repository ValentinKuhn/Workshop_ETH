from typing import List
import requests
import pandas as pd
import time
from pytickersymbols import PyTickerSymbols
import os


def get_stock_API(stock: str, apikey: str):
    API_URL = "https://www.alphavantage.co/query"
    data = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "outputsize": "compact",
        "datatype": "csv",
        "apikey": apikey,
    }
    response = requests.get(API_URL, data)
    if 'Invalid API call' in response.text:
        raise KeyError("Ticker not valid!")
    while '5 calls per minute' in response.text:
        time.sleep(60)
        response = requests.get(API_URL, data)
    return response.text




### ONLY IF NECESSARY COPY SOLUTION FROM HERE #####


def transform_api_output(api_result: str):
    text = [sub.split(",") for sub in api_result.split("\r\n")]
    header = text[0]
    body = text[1:]
    output = pd.DataFrame(body, columns=header).dropna()
    return output


def get_or_load(stock: str, apikey: str):
    data_dir = 'data/'
    data_files = os.listdir(data_dir)
    # Check if data folder is filled
    if len(data_files) > 0:
        data_buffered = pd.concat(
            [pd.read_csv(f'{data_dir}{file}', index_col=[0])
             for file in data_files])
        # Check if stock is available
        if stock in data_buffered.ticker.to_list():
            return data_buffered[data_buffered.ticker == stock]
    file = f'{data_dir}{stock}.csv'
    data = get_stock_prices(stock, apikey)
    data.to_csv(file)
    return data

def transform_hist_data(df: pd.DataFrame):
    output = df
    output['timestamp'] = output['timestamp'].str.replace('/', '-')
    output['close'] = output['close'].astype(float) / 100
    return output


def historical(stock: str, apikey: str):
    output = pd.DataFrame()
    hist_data_raw = get_or_load(stock, apikey, historical=True)
    hist_data = transform_hist_data(hist_data_raw)
    current_data = get_or_load(stock, apikey)
    output = pd.concat([current_data,hist_data])
    return output

def get_stocks(stocks: List[str], apikey: str):
    output = [historical(stock, apikey) for stock in stocks]
    return pd.concat(output)


def get_ticker_symbols():
    stock_data = PyTickerSymbols()
    stocks = stock_data.get_sp_100_nyc_yahoo_tickers()
    return stocks


def get_performance(df: pd.DataFrame):
    df = df.sort_values('timestamp', ascending=True)
    df['performance'] = df.close.diff(1)/df.close
    return df


def get_historical_prices(stock: str, apikey: str):
    API_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=full&datatype=csv&apikey={apikey}"
    response = requests.get(API_URL)
    if 'Invalid API call' in response.text:
        raise KeyError("Ticker not valid!")
    while '5 calls per minute' in response.text:
        time.sleep(60)
        response = requests.get(API_URL)
    text = [sub.split(",") for sub in response.text.split("\r\n")]
    output = pd.DataFrame(text[1:], columns=text[0]).dropna()
    output['ticker'] = stock
    output['timestamp'] = output['timestamp'].str.replace('-', '/')
    output['close'] = output['close'].astype(float) * 100
    return output[90:]