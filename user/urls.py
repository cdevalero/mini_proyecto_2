from django.urls import path
from django.urls.conf import include
from .views import Ordenar, addCliente, finalizarVenta

urlpatterns = [
    path('ordenar/', Ordenar, name='ordenar'),
    path('', addCliente, name='cliente'),
    path('venta/', finalizarVenta, name='venta'),
]
