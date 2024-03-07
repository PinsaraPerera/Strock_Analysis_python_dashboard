import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

st.title("Stock Price Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
button = st.sidebar.button("submit")

if button and ticker:
    data = yf.download(ticker, start=start_date, end=end_date)
    figure = px.line(data, x=data.index, y=data["Adj Close"], title=f"{ticker} Stock Price")
    st.plotly_chart(figure)

    pricing_data, fundemental_data, news = st.tabs(["Pricing", "Fundemental", "News"])

    with pricing_data:
        st.header("Pricing changes")
        data1 = data
        data1['% Change'] = data1['Adj Close']/ data1['Adj Close'].shift(1) - 1
        data1.dropna(inplace=True)
        st.write(data1)
        annual_returns = (data1['% Change'].mean() * 252) * 100
        st.write(f"The annual return is {annual_returns:.2f}%")
        sd = np.std(data1['% Change']) * np.sqrt(252) * 100 # annualized standard deviation without weekends
        st.write(f"The annualized standard deviation is {sd:.2f}%")

    with fundemental_data:
        st.write("Fundemental")

    with news:
        st.write("News")



