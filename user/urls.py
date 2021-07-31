from django.urls import path
from django.urls.conf import include
from .views import reportes, Ordenar, addCliente, finalizarVenta, verVentrasGenerales

urlpatterns = [
    path('ordenar/', Ordenar, name='ordenar'),
    path('', addCliente, name='cliente'),
    path('venta/', finalizarVenta, name='venta'),
    path('reporte_general/', reportes, name='reporte'),
    path('histroia/', verVentrasGenerales, name='histroia')
]
