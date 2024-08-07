from django.shortcuts import render

def crypto_dashboard(request):
    return render(request, 'crypto_dashboard.html')
