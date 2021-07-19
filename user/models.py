from django.db import models

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    identificacion = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank = True)
    direccion = models.TextField(max_length=300)

    def __str__(self):
        return self.identificacion


class Ingrediente(models.Model):
    ingrediente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.nombre


class Dimension(models.Model):
    dimension_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.nombre


class Galleta(models.Model):
    galleta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.nombre


class Bebida(models.Model):
    bebida_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    DOMICILIO = (
        ('S','Si'),
        ('N','No'),
    )
    METODO = (
        ('Efectivo','Efectivo'),
        ('Pago Movil','PM'),
        ('Zelle','Zelle'),
        ('Tarjeta','Tarjeta'),
    )
    venta_id = models.AutoField(primary_key=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(decimal_places=2, max_digits=5)
    delivery = models.CharField(choices=DOMICILIO, max_length=2)
    metodo_pago = models.CharField(choices=METODO, max_length=15)
    galleta_id = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=True, blank = True)

    def __str__(self):
        return self.venta_id


class Sandwich(models.Model):
    sandwich_id = models.AutoField(primary_key=True)
    dimension_id = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, blank = True)

    def __str__(self):
        return self.sandwich_id


class Contenido(models.Model):
    contenido_id = models.AutoField(primary_key=True)
    sandwich_id = models.ForeignKey(Sandwich, on_delete=models.CASCADE)
    ingrediente_id = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

    def __str__(self):
        return self.contenido_id


class Combo(models.Model):
    combo_id = models.AutoField(primary_key=True)
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)

    def __str__(self):
        return self.combo_id


class Cod_descuento(models.Model):
    cod_descuento_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20)
    porcentaje = models.IntegerField()

    def __str__(self):
        return self.codigo