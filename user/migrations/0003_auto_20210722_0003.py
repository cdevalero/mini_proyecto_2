# Generated by Django 3.2.5 on 2021-07-22 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210720_2211'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cod_descuento',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='fecha_nacimiento',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='galleta_id',
        ),
        migrations.AlterField(
            model_name='venta',
            name='delivery',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='venta',
            name='metodo_pago',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='Galleta',
        ),
    ]
