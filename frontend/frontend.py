import streamlit as st
import altair as alt
import os


st.set_page_config(page_title="Stock Dashboard", layout="wide")
page = st.sidebar.selectbox("Main Categorie", ["AAPL stock",
                                               'History',
                                               'One stock',
                                               'Many stocks',
                                               "Compare stocks"])
chart = (
        alt.Chart()
        .mark_line(point=True)
        .encode(
            x=alt.X("timestamp:O", timeUnit="yearmonthdate", title="date"),
            y="close:Q",
            color=alt.Color(
                "ticker",
                legend=alt.Legend(title="Stock"),
            ),
            size=alt.SizeValue(4),
        )
    )
from ipynb.fs.defs.workshop import get_stock_API, transform_api_output, get_stock_timeline, get_ticker_symbols, get_stocks, get_performance
def get_stock_prices(stock: str, apikey: str):
    api_result = get_stock_API(stock, apikey)
    output = transform_api_output(api_result)
    output['ticker'] = stock
    output['close'] = output['close'].astype(float)
    return output

if page == "AAPL stock":
    st.header("AAPL stock prices")
    df = get_stock_prices('AAPL', os.environ['API_KEY'])
    df_line = df[['timestamp', 'open']]
    df_line = df_line.set_index('timestamp')
    st.altair_chart(alt.layer(chart, data=df), use_container_width=True)

if page == "History":
    st.header("Show historical stock performance")
    ticker = 'AAPL'
    df = get_stock_timeline(ticker, os.environ['API_KEY'])
    st.altair_chart(alt.layer(chart, data=df), use_container_width=True)

if page == "One stock":
    st.header("Show stock performance")
    ticker = st.text_input("Ticker of stock:", value='IBM')
    df = get_stock_timeline(ticker, os.environ['API_KEY'])
    st.altair_chart(alt.layer(chart, data=df), use_container_width=True)

if page == "Many stocks":
    st.header("Compare stock performance")
    stocks = st.multiselect('Select stocks', options=get_ticker_symbols())
    if len(stocks) > 0:
        df = get_stocks(stocks, os.environ['API_KEY'])
        st.altair_chart(alt.layer(chart, data=df), use_container_width=True)

if page == "Compare stocks":
    st.header("Compare stock key figures")
    ticker_list = get_ticker_symbols()
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        stock1 = st.selectbox(
            'Select stock', options=ticker_list, index=3, key='1')
        df1 = get_stocks([stock1], os.environ['API_KEY'])
        df1 = get_performance(df1)
        earnings1 = df1.tail(1).close.to_list()[
            0] / df1.head(1).close.to_list()[0] - 1
        st.metric(
            f"Current Price:",
            "{:,.2f}$".format(df1.head(1).close.to_list()[0]),
            "{:,.2f}%".format(df1.tail(1).performance.to_list()[0]*100)
        )
        st.metric(
            f"Standard Deviation:",
            "{:,.2f}".format(
                df1.performance.std()*100
            )
        )

    with col_2:
        stock2 = st.selectbox(
            'Select stock', options=ticker_list, index=5, key='2')
        df2 = get_stocks([stock2], os.environ['API_KEY'])
        df2 = get_performance(df2)
        st.metric(
            f"Current Price:",
            "{:,.2f}$".format(df2.head(1).close.to_list()[0]),
            "{:,.2f}%".format(df2.tail(1).performance.to_list()[0]*100)
        )
        st.metric(
            f"Standard Deviation:",
            "{:,.2f}".format(
                df2.performance.std()*100
            )
        )

    with col_3:
        stock3 = st.selectbox('Select base stock',
                              options=ticker_list, index=7, key='3')
        df3 = get_stocks([stock3], os.environ['API_KEY'])
        df3 = get_performance(df3)
        st.metric(
            f"Current Price:",
            "{:,.2f}$".format(df3.head(1).close.to_list()[0]),
            "{:,.2f}%".format(df3.tail(1).performance.to_list()[0]*100)
        )
        st.metric(
            f"Standard Deviation:",
            "{:,.2f}".format(
                df3.performance.std()*100
            )
        )

    with col_4:
        stock4 = st.selectbox(
            'Select stock', options=ticker_list, index=14, key='4')
        df4 = get_stocks([stock4], os.environ['API_KEY'])
        df4 = get_performance(df4)
        st.metric(
            f"Current Price:",
            "{:,.2f}$".format(df4.head(1).close.to_list()[0]),
            "{:,.2f}%".format(df4.tail(1).performance.to_list()[0]*100)
        )
        st.metric(
            f"Standard Deviation:",
            "{:,.2f}".format(
                df4.performance.std()*100
            )
        )
