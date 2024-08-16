from django.db import models
from .coins import COINS

class Coin(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)

    def __str__(self):
        return self.name
    
    @classmethod

    def initialize_coins(cls):

        for coin in COINS:

            cls.objects.get_or_create(symbol=coin["symbol"], defaults={"name": coin["name"]})

class Strategy(models.Model):
    STRATEGY_CHOICES = [
        ('hold', 'Hold'),
        ('golden_cross', 'Golden Cross/Death Cross'),
    ]
    name = models.CharField(max_length=50, choices=STRATEGY_CHOICES)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    params = models.JSONField(default=dict)  # Strategy-specific settings

    def __str__(self):
        return f"{self.name} Strategy"

class Indicator(models.Model):
    INDICATOR_CHOICES = [
        ('ma', 'Moving Average'),
        ('ema', 'Exponential Moving Average'),
    ]
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='indicators')
    indicator_type = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    period = models.IntegerField()

    def __str__(self):
        return f"{self.indicator_type.upper()} {self.period}"
