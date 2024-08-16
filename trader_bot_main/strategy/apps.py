from django.apps import AppConfig


class StrategyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'strategy'
    def ready(self):
        from .models import Coin
        Coin.initialize_coins()  # Update or create coins
