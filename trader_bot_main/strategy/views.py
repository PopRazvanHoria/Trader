# strategy/views.py

from django.shortcuts import render
from .models import Strategy
from .forms import StrategyForm, CoinForm, IndicatorForm
from .backtest import execute_strategy

def strategy_view(request):
    strategy_form = StrategyForm()
    coin_form = CoinForm()
    indicator_form = IndicatorForm()

    results = None
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

    return render(request, 'strategy/strategy_view.html', {
        'strategy_form': strategy_form,
        'coin_form': coin_form,
        'indicator_form': indicator_form,
        'results': results
    })
