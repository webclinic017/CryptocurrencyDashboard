from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('buy', views.buy, name="buy"),
    path('sell', views.sell, name="sell"),
    path('history', views.history, name="history"),
    path('settings', views.settings, name="settings"),
    path('update', views.update, name="update"),
    path('balance', views.balance, name="balance"),
]