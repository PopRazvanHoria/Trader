import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import pandas as pd

from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse
import matplotlib
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
import os
from keras.layers import Dense, LSTM
import numpy as np

matplotlib.use('Agg')

def index(request):
    return render(request, 'trading/index.html')

def fetch_data(symbol, start_date=None, start_time=None, end_date=None, end_time=None, interval='1m'):
    if start_date and start_time and end_date and end_time:
        # Combine date and time into a single datetime string
        start_datetime_str = f"{start_date} {start_time}"
        end_datetime_str = f"{end_date} {end_time}"
        
        # Convert datetime strings to Unix timestamps in milliseconds
        start_timestamp = int(datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M').timestamp() * 1000)
        end_timestamp = int(datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M').timestamp() * 1000)
        url = 'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol + 'USDT',
            'interval': interval,
            'startTime': start_timestamp,
            'endTime': end_timestamp,
            'limit': 1000  # Maximum allowed limit for the request
        }
    else:
        # Default to using a fixed interval
        url = 'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol + 'USDT',
            'interval': interval,
            'limit': 1000
        }
    
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.astype({
        'open': 'float64',
        'high': 'float64',
        'low': 'float64',
        'close': 'float64',
        'volume': 'float64',
        'quote_asset_volume': 'float64',
        'number_of_trades': 'int64',
        'taker_buy_base_asset_volume': 'float64',
        'taker_buy_quote_asset_volume': 'float64'
    })
    
    return df

def plot_graph(request, symbol):
    start_date = request.GET.get('start_date')
    start_time = request.GET.get('start_time')
    end_date = request.GET.get('end_date')
    end_time = request.GET.get('end_time')
    strategy = request.GET.get('strategy', 'hold')
    amount = float(request.GET.get('amount', '0'))
    short_window = request.GET.get('short_window', 10)
    long_window = request.GET.get('long_window', 100)
    

    # Set default values if not provided
    if not start_date or not start_time:
        end_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=1)
        start_date = start_datetime.strftime('%Y-%m-%d')
        start_time = '00:00'
        end_date = end_datetime.strftime('%Y-%m-%d')
        end_time = '00:00'

    if not short_window or not long_window or short_window == '' or long_window == '':
        short_window = int(10)
        long_window = int(100)
        
    short_window = int(short_window)
    long_window = int(long_window)
  
    df = fetch_data(symbol, start_date, start_time, end_date, end_time)
  
    if df.empty:
        return HttpResponse('No data available', status=400)

    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['close'], label='Close Price', color = 'black')

    # Handle different strategies
    if strategy == 'hold':
        # Buy at start and sell at end
        buy_price = df['close'].iloc[0]
        sell_price = df['close'].iloc[-1]
        profit_percentage = ((sell_price - buy_price) / buy_price) * 100
        final_value = amount * (1 + profit_percentage / 100)

        plt.scatter(df['timestamp'].iloc[0], buy_price, marker='^', color='green', label='Buy (Start)', s = 100, zorder=10)
        plt.scatter(df['timestamp'].iloc[-1], sell_price, marker='v', color='red', label='Sell (End)', s = 100, zorder=10)

        plt.title(f'{symbol} Hold Strategy\nProfit: {profit_percentage:.2f}% Final Value: {final_value:.2f}')

    elif strategy == 'golden_cross':
        df['short_ema'] = df['close'].ewm(span=short_window, adjust=False).mean()
        df['long_ema'] = df['close'].ewm(span=long_window, adjust=False).mean()
       
        df['crossover'] = (df['short_ema'] >  df['long_ema']) & (df['short_ema'].shift(1) <=  df['long_ema'].shift(1))
        df['crossunder'] = (df['short_ema'] <  df['long_ema']) & (df['short_ema'].shift(1) >=  df['long_ema'].shift(1))
        
        df['crossover'] = df['crossover'].map(lambda x : int(x))
        df['crossunder'] = df['crossunder'].map(lambda x : -int(x))
        df['strategy'] = df['crossover'] + df['crossunder']

        capital = amount
        coins = 0
        trade_log = []
        
        for index, row in df.iterrows():
            if index < long_window :
                continue
            if row['strategy'] == 1:
                buy_price = row['close']
                trade_log.append({'action': 'buy', 'price': buy_price, 'timestamp' : row['timestamp'], 'index' : index})
                coins = capital / buy_price
                capital = 0

            elif row['strategy'] == -1 and coins != 0:
                sell_price = row['close']
                trade_log.append({'action': 'sell', 'price': sell_price, 'timestamp' : row['timestamp'], 'index' : index})
                capital = coins * sell_price
                coins = 0 

        plt.plot(df['timestamp'], df['short_ema'], label=f'{short_window}-Day EMA')
        plt.plot(df['timestamp'], df['long_ema'], label=f'{long_window}-Day EMA')

        print(trade_log)
        for trade in trade_log:

            if trade['action'] == 'buy':
                plt.scatter(trade['timestamp'],trade['price'], marker='^', color='green', s = 100,zorder=10)
            elif trade['action'] == 'sell':
                plt.scatter(trade['timestamp'],trade['price'], marker='v', color='red', s = 100,zorder=10)

        final_value = capital + coins * df['close'].iloc[-1]
        profit_percentage = ((final_value - amount) / amount) * 100

        plt.title(f'{symbol} Golden Cross/Death Cross Strategy\nProfit: {profit_percentage:.2f}% Final Value: {final_value:.2f}')

    elif strategy == 'lstm':
        # Prepare data for LSTM
        scaler = MinMaxScaler(feature_range=(0, 1))
        df['scaled_close'] = scaler.fit_transform(df['close'].values.reshape(-1, 1))

        # Prepare the training data
        look_back = 100
        x_train, y_train = [], []
        for i in range(look_back, len(df)):
            x_train.append(df['scaled_close'].iloc[i-look_back:i].values)
            y_train.append(df['scaled_close'].iloc[i])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Filepath to save/load model
        model_path = f'{symbol}_lstm_model.h5'
        # Load existing model if available
        if os.path.exists(model_path):
            model = load_model(model_path)
            print(f"Loaded existing model from {model_path}")
        else:
            # Build and train a new LSTM model
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(units=50))
            model.add(Dense(1))

            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
            
            # Save the model
            model.save(model_path)
            print(f"Saved new model to {model_path}")

        # Predicting future prices
        predictions = []
        for i in range(look_back, len(df)):
            input_data = df['scaled_close'].iloc[i-look_back:i].values
            input_data = np.reshape(input_data, (1, look_back, 1))
            predicted_price = model.predict(input_data)
            predictions.append(scaler.inverse_transform(predicted_price)[0][0])
        df = df.iloc[look_back:]
        df['predicted_close'] = predictions

        # Simulate trading
        capital = amount
        coins = 0
        trade_log = []

        for index, row in df.iterrows():
            if index == len(df) - 1:
                break  # Skip last row
            if row['predicted_close'] > row['close']:
                if coins == 0:
                    coins = capital / row['close']
                    capital = 0
                    trade_log.append({'action': 'buy', 'price': row['close'], 'timestamp': row['timestamp'], 'index': index})
            elif row['predicted_close'] < row['close']:
                if coins != 0:
                    capital = coins * row['close']
                    coins = 0
                    trade_log.append({'action': 'sell', 'price': row['close'], 'timestamp': row['timestamp'], 'index': index})

        # Final capital calculation
        final_value = capital + coins * df['close'].iloc[-1]
        profit_percentage = ((final_value - amount) / amount) * 100

        # Plot buy/sell points
        for trade in trade_log:
            if trade['action'] == 'buy':
                plt.scatter(trade['timestamp'], trade['price'], marker='^', color='green', s=100, zorder=10)
            elif trade['action'] == 'sell':
                plt.scatter(trade['timestamp'], trade['price'], marker='v', color='red', s=100, zorder=10)


        
        plt.title(f'{symbol} LSTM Strategy\nProfit: {profit_percentage:.2f}% Final Value: {final_value:.2f}')


    # EMA and MA plotting
    ema_values = request.GET.get('ema', '')
    if ema_values:
        ema_spans = [int(span) for span in ema_values.split(',') if span.strip().isdigit()]
        for span in ema_spans:
            ema = df['close'].ewm(span=span, adjust=False).mean()
            plt.plot(df['timestamp'], ema, label=f'EMA {span}')

    ma_values = request.GET.get('ma', '')
    if ma_values:
        ma_spans = [int(span) for span in ma_values.split(',') if span.strip().isdigit()]
        for span in ma_spans:
            ma = df['close'].rolling(window=span).mean()
            plt.plot(df['timestamp'], ma, label=f'MA {span}')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    graph_url = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()
    context = {
        'short_window': short_window,
        'long_window': long_window,
        'graph_url': graph_url,
        'start_date': start_date,
        'start_time': start_time,
        'end_date': end_date,
        'end_time': end_time,
        'ema': ema_values,
        'ma': ma_values
    }
    return render(request, 'trading/index.html', context)


def process_form(request):
    symbol = request.GET.get('symbol', 'BTC')
    amount = request.GET.get('amount', '100')

    # Calculate default dates and times
    end_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_datetime = end_datetime - timedelta(days=1)
    
    start_date = request.GET.get('start_date', start_datetime.strftime('%Y-%m-%d'))
    start_time = request.GET.get('start_time', '00:00')
    end_date = request.GET.get('end_date', end_datetime.strftime('%Y-%m-%d'))
    end_time = request.GET.get('end_time', '00:00')
    
    try:
        amount = float(amount)
    except ValueError:
        return render(request, 'trading/index.html', {'error': 'Invalid amount value'})
    
    if not start_date or not start_time or not end_date or not end_time:
        return render(request, 'trading/index.html', {'error': 'Start date, start time, end date, and end time are required'})
    
    df = fetch_data(symbol, start_date, start_time, end_date, end_time)
    # Example: Plot price graph
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['close'], label='Close Price')
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{symbol} Price Over Time')
    plt.legend()

    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    graph_url = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

    context = {
        'graph_url': graph_url,
        'start_date': start_date,
        'start_time': start_time,
        'end_date': end_date,
        'end_time': end_time,
        'amount': amount
    }
    
    return render(request, 'trading/index.html', context)
