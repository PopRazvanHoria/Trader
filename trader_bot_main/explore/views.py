from django.shortcuts import render

def crypto_dashboard(request):
    return render(request, 'explore/crypto_dashboard.html')
