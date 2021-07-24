from django.contrib import admin
from .models import Ingrediente, Cliente, Venta, Bebida, Sandwich, Dimension, Contenido


class VentaAdmin(admin.ModelAdmin):
    list_display = ('venta_id', 'cliente_id', 'fecha', 'total')
    list_filter = ['fecha']


admin.site.register([
    Ingrediente, 
    Cliente, 
    Bebida, 
    Sandwich, 
    Dimension,
    Contenido
    ]
)


admin.site.register(Venta,VentaAdmin)
