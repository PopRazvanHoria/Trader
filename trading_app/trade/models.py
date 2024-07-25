from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=255)
    balance = models.FloatField()

    def __str__(self):
        return self.username