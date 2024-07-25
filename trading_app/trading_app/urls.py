"""
URL configuration for trading_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from trade import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_account/', views.create_account, name='create_account'),
    path('trade/', views.trade, name='trade'),
    path('get_crypto_data/<str:symbol>/', views.get_crypto_data, name='get_crypto_data'),
    path('test_crypto_data/<symbol>', views.test_crypto_data, name='test_crypto_data')
    
]
