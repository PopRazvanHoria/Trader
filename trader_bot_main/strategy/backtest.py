from datetime import datetime
from .models import Strategy, Coin
import requests
import numpy as np


BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

def fetch_historical_data(symbol, interval, start_time, end_time):
    """Fetch historical data from Binance API."""
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(start_time.timestamp() * 1000),
        'endTime': int(end_time.timestamp() * 1000)
    }
    response = requests.get(BINANCE_API_URL, params=params)
    data = response.json()
    return [
        {
            'time': datetime.fromtimestamp(item[0] / 1000),
            'open': float(item[1]),
            'high': float(item[2]),
            'low': float(item[3]),
            'close': float(item[4]),
            'volume': float(item[5])
        }
        for item in data
    ]

def hold_strategy(strategy):
    results = {}
    for coin in strategy.coins.all():
        data = fetch_historical_data(f"{coin.symbol}USDT", '1d', strategy.start_time, strategy.end_time)
        if data:
            initial_price = data[0]['open']
            final_price = data[-1]['close']
            change_percentage = ((final_price - initial_price) / initial_price) * 100
            results[coin.symbol] = {
                'initial_price': initial_price,
                'final_price': final_price,
                'change_percentage': change_percentage,
                'profit_loss': change_percentage * float(coin.amount) / 100
            }
    return results

def calculate_moving_average(data, period):
    prices = [item['close'] for item in data]
    ma_values = np.convolve(prices, np.ones(period)/period, mode='valid')
    return ma_values.tolist()

def calculate_ema(data, period):
    prices = [item['close'] for item in data]
    ema_values = [sum(prices[:period]) / period]
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema_values.append((price - ema_values[-1]) * multiplier + ema_values[-1])
    return ema_values

def golden_cross_strategy(strategy):
    results = {}
    short_period = strategy.params.get('short_period', 50)
    long_period = strategy.params.get('long_period', 200)
    
    for coin in strategy.coins.all():
        data = fetch_historical_data(f"{coin.symbol}USDT", '1d', strategy.start_time, strategy.end_time)
        if data:
            short_ma = calculate_moving_average(data, short_period)
            long_ma = calculate_moving_average(data, long_period)

            golden_cross_points = []
            death_cross_points = []

            for i in range(1, len(short_ma)):
                if short_ma[i] > long_ma[i] and short_ma[i-1] <= long_ma[i-1]:
                    golden_cross_points.append(data[i + long_period - 1]['time'])
                elif short_ma[i] < long_ma[i] and short_ma[i-1] >= long_ma[i-1]:
                    death_cross_points.append(data[i + long_period - 1]['time'])

            results[coin.symbol] = {
                'golden_crosses': golden_cross_points,
                'death_crosses': death_cross_points
            }
    return results

def execute_strategy(strategy: Strategy):
    if strategy.name == 'hold':
        return hold_strategy(strategy)
    elif strategy.name == 'golden_cross':
        return golden_cross_strategy(strategy)
    # Add more strategies as needed
