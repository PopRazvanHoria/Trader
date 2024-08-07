from django.shortcuts import render
from .models import CryptoTrade

def home(request):
    trades = CryptoTrade.objects.all()
    return render(request, 'home.html', {'trades': trades})
