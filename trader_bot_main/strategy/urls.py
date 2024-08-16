from django.urls import path
from .views import strategy_view

urlpatterns = [
    path('test-strategy/', strategy_view, name='strategy_view'),
]
