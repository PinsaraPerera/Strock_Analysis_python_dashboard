import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import fundemental_data
import os
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv

load_dotenv()

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
        key = os.getenv("ALPHA_VANTAGE_API_KEY")
        fd = FundamentalData(key, output_format="pandas")
        st.subheader("Balance Sheet")
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.write(bs)
        st.subheader("Income Statement")
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is_ = income_statement.T[2:]
        is_.columns = list(income_statement.T.iloc[0])
        st.write(is_)
        st.subheader("Cash Flow")
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.write(cf)

    with news:
        st.write("News")
