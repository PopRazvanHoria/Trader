from django.shortcuts import render
import json
from datetime import datetime, timedelta
from .models import Coin
from .backtest import fetch_historical_data

def strategy_view(request):
    selected_coin = request.GET.get('coin', 'BTC')  # Default to 'BTC' if no coin is selected
    start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Fetch historical data
    data = fetch_historical_data(f"{selected_coin}USDT", '1d', start_date, end_date)
    
    # Prepare data for the chart
    dates = [entry['time'].strftime('%Y-%m-%d') for entry in data]
    prices = [entry['close'] for entry in data]

    return render(request, 'strategy_view.html', {
        'dates': json.dumps(dates),
        'prices': json.dumps(prices),
        'selected_coin': selected_coin
    })
