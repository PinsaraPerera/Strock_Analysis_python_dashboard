import streamlit as st
import pandas as pd
import numpy as np
import os
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Now you can access the variables using os.getenv
import os
variable = os.getenv('VARIABLE_NAME')


def set_fundemental_data(ticker):
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


