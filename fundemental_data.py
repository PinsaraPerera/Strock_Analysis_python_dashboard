from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Now you can access the variables using os.getenv
import os
variable = os.getenv('VARIABLE_NAME')


def get_fundemental_data():
    key = os.getenv('ALPHA_VANTAGE_API_KEY')
    fd = FundamentalData(key, output_format='pandas')
    st.subheader("Balance Sheet")

    return st.write(fd)