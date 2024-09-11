from django.urls import path
from .views import index, plot_graph, process_form
urlpatterns = [
    path('', index, name='index'),
    path('plot/<str:symbol>/', plot_graph, name='plot_graph'),
    path('process/', process_form, name='process_form'),
]
