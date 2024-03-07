import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import fundemental_data_view
import os
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv
from stocknews import StockNews
import sentiment_visualize

st.title("Stock Price Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
button = st.sidebar.button("submit")

if button and ticker:
    data = yf.download(ticker, start=start_date, end=end_date)
    figure = px.line(
        data, x=data.index, y=data["Adj Close"], title=f"{ticker} Stock Price"
    )
    st.plotly_chart(figure)

    pricing_data, fundemental_data, news = st.tabs(["Pricing", "Fundemental", "News"])

    with pricing_data:
        st.header("Pricing changes")
        data1 = data
        data1["% Change"] = data1["Adj Close"] / data1["Adj Close"].shift(1) - 1
        data1.dropna(inplace=True)
        st.write(data1)
        annual_returns = (data1["% Change"].mean() * 252) * 100
        st.write(f"The annual return is {annual_returns:.2f}%")
        sd = (
            np.std(data1["% Change"]) * np.sqrt(252) * 100
        )  # annualized standard deviation without weekends
        st.write(f"The annualized standard deviation is {sd:.2f}%")

    with fundemental_data:
        fundemental_data_view.set_fundemental_data(ticker)

    with news:
        st.header(f'News for {ticker}')
        news = StockNews(ticker, save_news=False)
        df_news = news.read_rss()

        for i in range(10):
            st.subheader(f'News {i+1}')
            st.write(df_news['published'][i])
            st.write(df_news['title'][i])
            st.write(df_news['summary'][i])


            title_sentiment = df_news['sentiment_title'][i]
            st.write(f'Title sentiment: {title_sentiment}')
            news_sentiment = df_news['sentiment_summary'][i]
            st.write(f'News sentiment: {news_sentiment}')

            sentiment_visualize.set_sentiment_score(news_sentiment)


            