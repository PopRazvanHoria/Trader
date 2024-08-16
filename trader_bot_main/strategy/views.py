from django.shortcuts import render, redirect
from .models import Strategy, Coin
from .forms import StrategyForm, CoinForm, IndicatorForm
from .backtest import execute_strategy

def strategy_view(request):
    results = None
    if request.method == "POST":
        strategy_form = StrategyForm(request.POST)
        indicator_form = IndicatorForm(request.POST)

        if strategy_form.is_valid() and indicator_form.is_valid():
            strategy = strategy_form.save()
            # Add coins to the strategy
            strategy.coins.set(strategy_form.cleaned_data['coins'])
            indicator_form.instance.strategy = strategy
            indicator_form.save()

            results = execute_strategy(strategy)

            # Redirect to avoid resubmission on refresh
            return redirect('strategy_view')
    else:
        strategy_form = StrategyForm()
        indicator_form = IndicatorForm()

    return render(request, 'strategy_view.html', {
        'strategy_form': strategy_form,
        'indicator_form': indicator_form,
        'results': results
    })
