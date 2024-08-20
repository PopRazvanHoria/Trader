from django.urls import path
from .views import index, fetch_crypto_data, plot_graph, process_form
urlpatterns = [
    path('', index, name='index'),
    path('fetch/<str:symbol>/', fetch_crypto_data, name='fetch_crypto_data'),
    path('plot/<str:symbol>/', plot_graph, name='plot_graph'),
    path('process/', process_form, name='process_form'),
]
