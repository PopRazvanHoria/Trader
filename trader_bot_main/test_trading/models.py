from django.db import models

class CryptoCurrency(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.symbol
