from graphs import *


def generate_stock_page(df):
    # generate_vwap_graph(df)
    # generate_macd_graph(df)
    # generate_supertrend_graph(df)
    # generate_rsi_graph(df)
    print(type(df))
    result = get_prediction(df)
    return result


def get_prediction(df):
    return 0
