from django.urls import path
from .views import index, fetch_crypto_data, plot_graph, process_form, hold_strategy, golden_cross_strategy

urlpatterns = [
    path('', index, name='index'),
    path('fetch/<str:symbol>/', fetch_crypto_data, name='fetch_crypto_data'),
    path('plot/<str:symbol>/', plot_graph, name='plot_graph'),
    path('process/', process_form, name='process_form'),
    path('strategy/hold/<str:symbol>/<str:amount>/<str:timespan>/', hold_strategy, name='hold_strategy'),
    path('strategy/golden_cross/<int:short_window>/<int:long_window>/<str:symbol>/', golden_cross_strategy, name='golden_cross_strategy'),
]
