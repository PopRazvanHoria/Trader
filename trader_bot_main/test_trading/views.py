import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render


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
from io import BytesIO
import base64
from django.http import HttpResponse

@api_view(['GET'])
def plot_graph(request, symbol):
    interval = request.GET.get('interval', '1d')
    df = fetch_data(symbol, interval=interval)
    
    if df.empty:
        return JsonResponse({'error': 'No data available'}, status=400)
    
    # Convert necessary columns to the correct data type
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)  # Set timestamp as the index
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['close'], label='Close Price')

    ema_span = request.GET.get('ema')
    if ema_span:
        ema = df['close'].ewm(span=int(ema_span), adjust=False).mean()
        plt.plot(df.index, ema, label=f'EMA {ema_span}')
    
    ma_span = request.GET.get('ma')
    if ma_span:
        ma = df['close'].rolling(window=int(ma_span)).mean()
        plt.plot(df.index, ma, label=f'MA {ma_span}')
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{symbol} Price Over Time')
    plt.legend()
    
    # Save plot to a temporary file
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Return image as a response
    return HttpResponse(buffer, content_type='image/png')


def hold_strategy(request, symbol, amount, timespan):
    try:
        amount = float(amount)  # Convert amount from string to float
    except ValueError:
        return JsonResponse({'error': 'Invalid amount value'}, status=400)

    # Fetch data and apply the strategy
    df = fetch_data(symbol)  # implement fetch_data to get DataFrame

    # Example: Calculate investment value
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

import requests
import pandas as pd

def fetch_data(symbol, interval='1d'):
    # Ensure 'USDT' is appended only if it's not already included
    if not symbol.endswith('USDT'):
        symbol += 'USDT'
    
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1000
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    
    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    
    return df


def index(request):
    return render(request, 'trading/index.html')

def process_form(request):
    symbol = request.GET.get('symbol', 'BTCUSDT')
    amount = request.GET.get('amount', '0')
    timespan = request.GET.get('timespan', '1d')

    try:
        amount = float(amount)
    except ValueError:
        return render(request, 'trading/index.html', {'error': 'Invalid amount value'})
    
    df = fetch_data(symbol, interval=timespan)
    
    # Example: Plot price graph
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['close'], label='Close Price')
    
    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    graph_url = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'trading/index.html', {'graph_url': graph_url})