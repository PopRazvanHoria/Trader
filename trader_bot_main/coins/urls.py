from django.urls import path
from . import views

urlpatterns = [
    path('<str:symbol>/', views.coin_detail, name='coin_detail'),
]
