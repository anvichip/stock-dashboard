import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

def generate_vwap_graph(dataframe):
    # Calculate VWAP
    dataframe['TP'] = (dataframe['High'] + dataframe['Low'] + dataframe['Close']) / 3
    dataframe['TPV'] = dataframe['TP'] * dataframe['Volume']
    dataframe['Cumulative TPV'] = dataframe['TPV'].cumsum()
    dataframe['Cumulative Volume'] = dataframe['Volume'].cumsum()
    dataframe['VWAP'] = dataframe['Cumulative TPV'] / dataframe['Cumulative Volume']

    # Plot VWAP
    plt.figure(figsize=(12, 6))
    plt.plot(dataframe['VWAP'], label='VWAP', color='blue')
    plt.title('Volume Weighted Average Price (VWAP)')
    plt.xlabel('Date')
    plt.ylabel('VWAP')
    plt.legend()

    # Save the graph
    plt.savefig('vwap_graph.png')
    plt.show()



def generate_supertrend_graph(dataframe, period=7, multiplier=3):
    # Calculate Supertrend
    dataframe['supertrend'] = ta.supertrend(dataframe['High'], dataframe['Low'], dataframe['Close'], length=period, multiplier=multiplier)

    # Plot Supertrend
    plt.figure(figsize=(12, 6))
    plt.plot(dataframe['Close'], label='Close Price', color='blue')
    plt.plot(dataframe['supertrend'], label='Supertrend', color='red')
    plt.title('Supertrend Indicator')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Save the graph
    plt.savefig('graph_supertrend.png')
    plt.show()


import math

def backtest_supertrend(df, investment):
    is_uptrend = df['Supertrend']
    close = df['Close']
    
    # initial condition
    in_position = False
    equity = investment
    commission = 5
    share = 0
    entry = []
    exit = []
    
    for i in range(2, len(df) - 1):  # Fix the loop range
        # if not in position & price is on uptrend -> buy
        if not in_position and is_uptrend[i]:
            share = math.floor(equity / close[i] / 100) * 100
            equity -= share * close[i]
            entry.append((i, close[i]))
            in_position = True
            print(f'Buy {share} shares at {round(close[i],2)} on {df.index[i].strftime("%Y/%m/%d")}')
        # if in position & price is not on uptrend -> sell
        elif in_position and not is_uptrend[i]:
            equity += share * close[i] - commission
            exit.append((i, close[i]))
            in_position = False
            print(f'Sell at {round(close[i],2)} on {df.index[i].strftime("%Y/%m/%d")}')
    
    # if still in position -> sell all shares 
    if in_position:
        equity += share * close[-1] - commission  # Use the correct index
    
    earning = equity - investment
    roi = round(earning/investment*100, 2)
    print(f'Earning from investing $100k is ${round(earning, 2)} (ROI = {roi}%)')
    return entry, exit, equity, roi

#entry, exit, final_equity, roi = backtest_supertrend(df, 100000)



def generate_macd_graph(dataframe, short_window=12, long_window=26, signal_window=9):
    # Calculate short-term exponential moving average
    dataframe['ema_short'] = dataframe['Close'].ewm(span=short_window, adjust=False).mean()

    # Calculate long-term exponential moving average
    dataframe['ema_long'] = dataframe['Close'].ewm(span=long_window, adjust=False).mean()

    # Calculate MACD Line
    dataframe['macd_line'] = dataframe['ema_short'] - dataframe['ema_long']

    # Calculate Signal Line
    dataframe['macd_signal'] = dataframe['macd_line'].ewm(span=signal_window, adjust=False).mean()

    # Plot MACD
    plt.figure(figsize=(12, 6))
    plt.plot(dataframe['macd_line'], label='MACD Line', color='blue')
    plt.plot(dataframe['macd_signal'], label='Signal Line', color='orange')
    plt.title('MACD Indicator')
    plt.xlabel('Date')
    plt.ylabel('MACD Value')
    plt.legend()

    # Save the graph
    plt.savefig('macd_graph.png')
    plt.show()

# Example usage:
# Assuming you have a DataFrame named 'df' with columns like 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'
# generate_macd_graph(df)



def generate_rsi_graph(dataframe, window=14):
    # Calculate RSI
    close_price_diff = dataframe['Close'].diff(1)
    gain = close_price_diff.where(close_price_diff > 0, 0)
    loss = -close_price_diff.where(close_price_diff < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    relative_strength = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + relative_strength))

    # Plot RSI
    plt.figure(figsize=(12, 6))
    plt.plot(rsi, label='RSI', color='purple')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI Value')
    plt.axhline(y=70, color='red', linestyle='--', label='Overbought Threshold (70)')
    plt.axhline(y=30, color='green', linestyle='--', label='Oversold Threshold (30)')
    plt.legend()

    # Save the graph
    plt.savefig('rsi_graph.png')
    plt.show()

# Example usage:
# Assuming you have a DataFrame named 'df' with columns like 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'
# generate_rsi_graph(df)
