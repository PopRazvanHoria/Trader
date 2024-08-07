from django.urls import path
from .views import crypto_dashboard

urlpatterns = [
    path('dashboard/', crypto_dashboard, name='crypto_dashboard'),
]
