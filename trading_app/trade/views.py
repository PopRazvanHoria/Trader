from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from trade.utils import data_retrieval, trading_execution, trading_strategies


def index(request):
    return render(request, 'index.html')

def dashboard(request):
    accounts = Account.objects.all()
    return render(request, 'dashboard.html', {'accounts': accounts})

def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        balance = request.POST['balance']
        Account.objects.create(username=username, balance=balance)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')

def get_crypto_data(request, symbol):
    data = data_retrieval.test_dataretrival(symbol)
    return render(request, 'crypto_data.html', {'data': data})

def trade(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        qty = request.POST['qty']
        side = request.POST['side']
        type = request.POST['type']
        response = trading_execution.place_order(symbol, qty, side, type, 'gtc')
        messages.success(request, 'Trade executed successfully!')
        return redirect('dashboard')

def test_crypto_data(request):
    data = data_retrieval.test_dataretrival()
    return render(request, 'test.html')