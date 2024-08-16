from django import forms
from .models import Strategy, Coin, Indicator
from .coins import get_coin_choices

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'start_time', 'end_time', 'coin']

class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ['symbol', 'name', 'amount']

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['indicator_type', 'period']