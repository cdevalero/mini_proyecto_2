from django.contrib import admin
from .models import Ingrediente, Cliente, Venta, Bebida, Sandwich, Dimension, Contenido

admin.site.register(
    [Ingrediente, 
    Cliente, 
    Venta,  
    Bebida, 
    Sandwich, 
    Dimension,
    Contenido,
    ]
)
