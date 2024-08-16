# views.py

from django.shortcuts import render
from .models import Strategy, Coin
from .forms import StrategyForm, CoinForm, IndicatorForm
from .backtest import execute_strategy, fetch_historical_data
from datetime import datetime

def strategy_view(request):
    strategy_form = StrategyForm()
    coin_form = CoinForm()
    indicator_form = IndicatorForm()

    results = None
    coins = Coin.objects.all()  # Retrieve all coins
    chart_data = {}

    if request.method == "POST":
        strategy_form = StrategyForm(request.POST)
        coin_form = CoinForm(request.POST)
        indicator_form = IndicatorForm(request.POST)

        if strategy_form.is_valid() and coin_form.is_valid():
            strategy = strategy_form.save()
            strategy.coins.add(coin_form.save())
            indicator_form.instance.strategy = strategy
            if indicator_form.is_valid():
                indicator_form.save()

            results = execute_strategy(strategy)
            
            # Fetch historical data for the selected coins
            selected_coins = strategy.coins.all()
            for coin in selected_coins:
                data = fetch_historical_data(f"{coin.symbol}USDT", '1d', strategy.start_time, strategy.end_time)
                chart_data[coin.symbol] = {
                    'dates': [item['time'].strftime('%Y-%m-%d') for item in data],
                    'prices': [item['close'] for item in data]
                }

    return render(request, 'strategy_view.html', {
        'strategy_form': strategy_form,
        'coin_form': coin_form,
        'indicator_form': indicator_form,
        'results': results,
        'coins': coins,
        'chart_data': chart_data  # Pass chart data to the template
    })
