from typing import List
import pandas as pd
import os
import requests
import time

def get_historical_data(stock: str, apikey: str):
    # Define folder, filename and file path
    file_name = f'{stock}.csv'
    data_dir = 'data/hist/'
    file_path = f'{data_dir}{file_name}'
    
    # Check if stock already in data lake
    if file_name in os.listdir(data_dir):
        data = pd.read_csv(file_path, index_col=0)
        return data
    
    # If stock not found locally, return API call
    data = get_historical_data_API(stock, apikey)
    if 'timestamp' in data.columns:
        data.to_csv(file_path)
        data['close'] = data['close'].astype(float)
        return data
    else:
        raise KeyError('Column timestamp not in dataframe!')


def get_historical_data_API(stock: str, apikey: str):
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
    return output[100:]



