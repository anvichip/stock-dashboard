from graphs import *
from arima_runner import *


def generate_stock_page(df):
    generate_vwap_graph(df)
    generate_macd_graph(df)
    generate_supertrend_graph(df)
    generate_rsi_graph(df)
    print(type(df))
    # result = get_prediction(df)
    result = run_this(df)
    return result


# def get_prediction(df):
#     return 0
