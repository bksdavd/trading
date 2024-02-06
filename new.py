import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
   
def fetch_stock_data(symbol):
    api_key = 'ZHPGKCDJQHJRXOA6'  
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (5min)' in data:
        return data['Time Series (5min)']
    else:
        return None

def plot_intraday_prices(data, symbol):
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in data.keys()]
    prices = [float(entry['4. close']) for entry in data.values()]

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, prices, label='Intraday Prices')
    plt.title(f'Intraday Prices for {symbol}')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def SMA_20(data, timestamps):
    sma_20 = [sum(prices[i-20:i])/20 for i in range(20, len(prices))]
    plt.plot(timestamps[20:], sma_20, label='SMA (20)')

def RSI(data, timestamps):
    rsi_14 = calculate_rsi(prices, 14)
    plt.axhline(y=70, color='r', linestyle='--', label='Overbought')
    plt.axhline(y=30, color='g', linestyle='--', label='Oversold')
    plt.plot(timestamps[14:], rsi_14, label='RSI (14)')

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100./(1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i-1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

    return rsi

stock_symbol = input('Enter stock symbol: ') 
stock_data = fetch_stock_data(stock_symbol)
if stock_data:
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in stock_data.keys()]
    prices = [float(entry['4. close']) for entry in stock_data.values()]

    plot_intraday_prices(stock_data, stock_symbol)
    SMA_20(stock_data, timestamps)
    RSI(stock_data, timestamps[14:])
    
    plt.show()
else:
    print(f"Failed to fetch data for {stock_symbol}")