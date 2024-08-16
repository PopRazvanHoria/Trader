from django.urls import path
from .views import fetch_crypto_data, plot_graph, hold_strategy, golden_cross_strategy

urlpatterns = [
    path('data/<str:symbol>/', fetch_crypto_data, name='fetch_crypto_data'),
    path('plot/<str:symbol>/', plot_graph, name='plot_graph'),
    path('strategy/hold/<str:symbol>/<float:amount>/<str:timespan>/', hold_strategy, name='hold_strategy'),
    path('strategy/golden-cross/<str:symbol>/<int:short_window>/<int:long_window>/', golden_cross_strategy, name='golden_cross_strategy'),
]
