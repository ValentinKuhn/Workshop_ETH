from typing import List
import requests
import pandas as pd
import time
from pytickersymbols import PyTickerSymbols
import os

### ONLY IF NECESSARY COPY SOLUTION FROM HERE #####


def transform_api_output(api_result: str):
    text = [sub.split(",") for sub in api_result.split("\r\n")]
    header = text[0]
    body = text[1:]
    output = pd.DataFrame(data=body, columns=header).dropna()
    return output


def transform_hist_data(df: pd.DataFrame):
    output = df
    output['timestamp'] = output['timestamp'].str.replace('/', '-')
    output['close'] = output['close'].astype(float) / 100
    return output


def get_stocks(stocks: List[str], apikey: str):
    output = [get_stock_timeline(stock, apikey) for stock in stocks]
    return pd.concat(output)



def get_performance(df: pd.DataFrame):
    df = df.sort_values('timestamp', ascending=True)
    df['performance'] = df.close.diff(1)/df.close
    return df
