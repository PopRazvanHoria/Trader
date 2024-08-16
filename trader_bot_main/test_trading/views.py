import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import pandas as pd

@api_view(['GET'])
def fetch_crypto_data(request, symbol):
    interval = request.GET.get('interval', '1d')  # default to 1 day
    url = f'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol + 'USDT',  # assuming USDT for simplicity
        'interval': interval,
        'limit': 1000
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    return JsonResponse(df.to_dict(orient='index'))

import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse

@api_view(['GET'])
def plot_graph(request, symbol):
    df = fetch_data(symbol)  # implement fetch_data to get DataFrame

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['close'], label='Close Price')
    
    # Add indicators like EMA here
    # Example: EMA
    ema = df['close'].ewm(span=20, adjust=False).mean()
    plt.plot(df.index, ema, label='EMA 20')
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{symbol} Price History')
    plt.legend()

    # Save to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')

def hold_strategy(request, symbol, amount, timespan):
    df = fetch_data(symbol)  # implement fetch_data to get DataFrame

    # Simple Hold Strategy Logic
    current_price = df['close'].iloc[-1]
    investment_value = amount * current_price
    return JsonResponse({'investment_value': investment_value})

def golden_cross_strategy(request, symbol, short_window, long_window):
    df = fetch_data(symbol)  # implement fetch_data to get DataFrame

    short_ema = df['close'].ewm(span=short_window, adjust=False).mean()
    long_ema = df['close'].ewm(span=long_window, adjust=False).mean()
    
    # Identify golden cross
    crossover = (short_ema > long_ema) & (short_ema.shift(1) <= long_ema.shift(1))
    signals = df.loc[crossover, 'close']

    return JsonResponse({'golden_cross_signals': signals.to_dict()})

