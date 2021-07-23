from django.db import models

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    identificacion = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.TextField(max_length=300)

    def __str__(self):
        return str(self.identificacion)


class Ingrediente(models.Model):
    ingrediente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def __str__(self):
        return self.nombre


class Dimension(models.Model):
    dimension_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def __str__(self):
        return self.nombre

class Bebida(models.Model):
    bebida_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    venta_id = models.AutoField(primary_key=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.FloatField()
    delivery = models.CharField(max_length=5)
    metodo_pago = models.CharField(max_length=20)

    def __str__(self):
        return str(self.venta_id)


class Sandwich(models.Model):
    sandwich_id = models.AutoField(primary_key=True)
    dimension_id = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, blank = True)
    bebida_id = models.ForeignKey(Bebida, on_delete=models.CASCADE, null=True, blank = True)

    def __str__(self):
        return str(self.sandwich_id)


class Contenido(models.Model):
    contenido_id = models.AutoField(primary_key=True)
    sandwich_id = models.ForeignKey(Sandwich, on_delete=models.CASCADE)
    ingrediente_id = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.contenido_id)
