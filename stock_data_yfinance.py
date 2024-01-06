import pandas as pd
import yfinance as yf
import numpy as np
import pandas as pd
from graphs import *

#Get Stocks using stock code and days
def get_stocks(stock_code, days):
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=days)

    # Download stock data using yfinance
    stock_data = yf.download(stock_code, start=start_date, end=end_date)

    # Reset index and create a 'Date' column from the index
    stock_data_reset = stock_data.reset_index()
    stock_data_reset['Date'] = stock_data_reset['Date'].dt.date
    stock_data_reset.to_csv('data.csv')
    return stock_data_reset


#df = get_stocks("GOOG", 365)

# generate_vwap_graph(df)
# generate_macd_graph(df)
# generate_supertrend_graph(df)
# generate_rsi_graph(df)