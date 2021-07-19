from django.contrib import admin
from .models import Ingrediente, Cliente, Venta, Combo, Bebida, Sandwich, Dimension, Contenido, Cod_descuento, Galleta

admin.site.register(
    [Ingrediente, 
    Cliente, 
    Venta, 
    Combo, 
    Bebida, 
    Sandwich, 
    Dimension,
    Contenido,
    Cod_descuento,
    Galleta, 
    ]
)
