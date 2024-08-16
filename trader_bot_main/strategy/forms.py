from django import forms
from .models import Strategy, Coin, Indicator

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'coin', 'start_time', 'end_time', 'params']

class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ['symbol', 'name', 'amount']

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['indicator_type', 'period']
