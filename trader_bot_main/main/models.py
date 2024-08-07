from django.db import models

class CryptoTrade(models.Model):
    symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.amount} @ {self.price}"
