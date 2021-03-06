from django.db import connection
from .forms import FormCliente
from datetime import date
from django.shortcuts import redirect, render
from django.db.models import Count
from .models import Cliente as comprador, Venta as vetanrealizada, Sandwich as emparerado, Contenido as tablacontenido, Ingrediente as tablaingrediente, Dimension as tabladimension

def addCliente(request):
   '''
   Envia y recibe el formulario de cliente para empezar el proceso de compra
   '''
   if request.method == 'POST':
      form = FormCliente(request.POST)
      identificacion = form.data['identificacion']
      nombre = form.data['nombre']
      apellido = form.data['apellido']
      direccion = form.data['direccion']
      request.session['cliente'] = {'i': identificacion, 'n': nombre, 'a': apellido, 'd': direccion}
      return redirect('ordenar')

   request.session['cliente'] = []
   request.session['sandwiches'] = []
   context = FormCliente()
   return render(request, 'cliente.html', {'context': context})


def Ordenar(request):
   '''
   Recibe el formulario del sandwich que se esta ordenando
   '''
   if request.method == 'POST':
      sandwiche = makeSandwich(request)
      if 'terminar' in request.POST:
         lista = request.session['sandwiches']
         lista.append(sandwiche)
         request.session['sandwiches'] = lista
         return redirect('venta')
      elif 'agregar' in request.POST: 
         lista = request.session['sandwiches']
         lista.append(sandwiche)
         request.session['sandwiches'] = lista
         sandwiches, precio = traducir(request, request.session['sandwiches'])
         return render(request, 'ordenar.html', {'sandwiches':sandwiches, 'precio':precio})
         
   return render(request, 'ordenar.html')


def makeSandwich(request):
   '''
   Genera una lista donde se almacena un sandwich especifico 
   '''
   sandwich = []
   try:
      sandwich.append(request.POST['size'])
   except:
      pass
   try:
      sandwich.append(request.POST['jam'])
   except:
      pass
   try:
      sandwich.append(request.POST['cha'])
   except:
      pass
   try:
      sandwich.append(request.POST['pim'])
   except:
      pass
   try:
      sandwich.append(request.POST['dqq'])
   except:
      pass
   try:
      sandwich.append(request.POST['ace'])
   except:
      pass
   try:
      sandwich.append(request.POST['pep'])
   except:
      pass
   try:
      sandwich.append(request.POST['sal'])
   except:
      pass
   return sandwich


def traducir(request, listas):
   '''
   interpreta los codigos de productos enviados del front 
   '''
   sandwiches = []
   total = 0
   n = 1
   for lista in listas:
      sandwich = {}
      sandwich['numero'] = n
      ingredientes = []
      precio = 0
      if len(lista) == 1:
         ingredientes.append('Queso')
      for parte in lista:
         if parte == 'ind':
            sandwich['size'] = 'Individual'
            precio=precio+280
         elif parte == 'dob':
            sandwich['size'] = 'Doble'
            precio=precio+430
         elif parte == 'tri':
            sandwich['size'] = 'Triple'
            precio=precio+580
         elif parte == 'jam':
            ingredientes.append('Jam??n')
            precio=precio+40
         elif parte == 'cha':
            ingredientes.append('Champi??ones')
            precio=precio+35
         elif parte == 'dqq':
            ingredientes.append('Doble queso')
            precio=precio+40
         elif parte == 'ace':
            ingredientes.append('Aceitunas')
            precio=precio+57.5
         elif parte == 'pep':
            ingredientes.append('Pepperoni')
            precio=precio+38.5
         elif parte == 'pim':
            ingredientes.append('Piment??n')
            precio=precio+30
         elif parte == 'sal':
            ingredientes.append('Salchich??n')
            precio=precio+62.5
            
      sandwich['precio'] = precio
      sandwich['ingrediente'] = ingredientes
      n=n+1
      sandwiches.append(sandwich)
      total = total+precio

   return sandwiches, total


def finalizarVenta(request):
   '''
   Concreta la venta del una orden guardando los datos en la BD
   '''
   cliente = request.session['cliente']
   sandwiches, precio = traducir(request, request.session['sandwiches'])
   if request.method == 'POST':
      deli = request.POST['deli']
      metodo = request.POST['metodo']

      try:
         test = comprador.objects.get(identificacion=int(cliente['i']))
      except comprador.DoesNotExist:
         guardar_cliente(request, cliente)

      guardar_venta(request, deli, metodo, float(precio), int(cliente['i']))

      guardar_sandwiches(request, sandwiches)

      return redirect('cliente')

   return render(request, 'finalizar_venta.html', {'cliente':cliente, 'sandwiches':sandwiches, 'precio':precio})


def guardar_cliente(request, cliente):
   '''
   Insert de cliente en la tabla cliente
   '''
   with connection.cursor() as cursor:
        cursor.execute (
         "INSERT INTO user_cliente(nombre, apellido, direccion, identificacion) VALUES (%s, %s, %s, %s);",
        [cliente['n'], cliente['a'], cliente['d'], int(cliente['i'])])


def guardar_venta(request, deli, metodo, precio, cliente):
   '''
   Insert de venta en la tabla venta
   '''
   id = comprador.objects.get(identificacion=cliente)
   with connection.cursor() as cursor:
        cursor.execute (
         "INSERT INTO user_venta(cliente_id_id, fecha, total, delivery, metodo_pago) VALUES (%s, date('now'), %s, %s, %s);",
        [id.cliente_id, precio, deli, metodo])


def guardar_sandwiches(request, sandwiches):
   '''
   Insert de Sandwiches en la tabla sandwich e ingredientes en contenido
   '''
   venta = obtenerVenta(request)
   venta= venta[0]
   for s in sandwiches: 
      with connection.cursor() as cursor:
        cursor.execute (
         "INSERT INTO user_sandwich(venta_id_id, dimension_id_id) VALUES (%s, (SELECT dimension_id FROM user_dimension WHERE nombre=%s));",
        [venta, s['size']])
      sw = emparerado.objects.last()
      sw = sw.sandwich_id
      for i in s['ingrediente']:
         with connection.cursor() as cursor:
            cursor.execute (
            "INSERT INTO user_contenido(sandwich_id_id, ingrediente_id_id) VALUES (%s, (SELECT ingrediente_id FROM user_ingrediente WHERE nombre=%s));",
            [sw, i])


def obtenerVenta(request):
   '''
   Select explicto para obtener la cantidad de ventas registradas en la base de datos
   '''
   with connection.cursor() as cursor:
      cursor.execute ("SELECT MAX(venta_id) FROM user_venta;")
      row = cursor.fetchone()
   return row


# -------------- #

def verVentrasGenerales(request):
   '''
   Permite ver en detalle las ventas realizadas
   '''
   context = []
   vista = {}

   ventas = vetanrealizada.objects.all().order_by('-venta_id')
   
   for v in ventas: 
      vista['venta_id'] = v.venta_id
      fecha = v.fecha
      vista['venta_fecha'] = fecha.strftime("%d-%m-%Y")
      vista['venta_total'] = v.total
      vista['venta_deli'] = v.delivery
      vista['venta_pago'] = v.metodo_pago
      vista['cliente'] = v.cliente_id.identificacion
      vista['cliente_nombre'] = v.cliente_id.nombre + ' ' + v.cliente_id.apellido
      vista['cliente_direccion'] = v.cliente_id.direccion
      
      ordenes = []
      sandwiches = emparerado.objects.filter(venta_id=v.venta_id)
      for s in sandwiches:
         orden = {}
         sw = s.sandwich_id
         orden['size'] = s.dimension_id.nombre
         ingrediente = []
         contenido = tablacontenido.objects.filter(sandwich_id=s.sandwich_id)
         for c in contenido:
            ingrediente.append(c.ingrediente_id.nombre)
            orden['ingrediente'] = ingrediente
         ordenes.append(orden)
      vista['ordenes'] = ordenes
      context.append(vista)
      vista={}
      
   return render(request, 'historico.html', {'context': context})


def reportes(request):
   '''
   Genera los reportes de la aplicacion
   '''
   n = 0
   ventas_totales = vetanrealizada.objects.count()
   ventas_sw_totales = emparerado.objects.count()

   ventas_dia = vetanrealizada.objects.values('fecha').annotate(count=Count('fecha')).order_by()
   for v in ventas_dia:
      v['fecha'] = v['fecha'].strftime("%d-%m-%Y")


   with connection.cursor() as cursor:
      cursor.execute (
      "SELECT count(s.sandwich_id), v.fecha FROM user_sandwich s, user_venta v WHERE s.venta_id_id = v.venta_id GROUP BY v.fecha;")
      ventas_sw_dia = cursor.fetchall()
   temp = {}
   v_temp = []
   for v in ventas_sw_dia:
      temp['fecha'] = v[1].strftime("%d-%m-%Y")
      temp['count'] = v[0]
      v_temp.append(temp)
      temp = {}
   ventas_sw_dia = v_temp

   ventas_size = emparerado.objects.values('dimension_id').annotate(count=Count('dimension_id')).order_by()

   ventas_ingrediente = tablacontenido.objects.values('ingrediente_id').annotate(count=Count('ingrediente_id')).order_by()

   ventas_cliente = vetanrealizada.objects.values('cliente_id').annotate(count=Count('cliente_id')).order_by('-count')
   clientes = comprador.objects.all()

   with connection.cursor() as cursor:
      cursor.execute (
      "SELECT count(s.sandwich_id), v.cliente_id_id FROM user_sandwich s, user_venta v WHERE s.venta_id_id = v.venta_id GROUP BY v.cliente_id_id ORDER BY count(s.sandwich_id) DESC;")
      ventas_sw_cliente = cursor.fetchall()
   temp = {}
   v_temp = []
   for v in ventas_sw_cliente:
      temp['cliente_id'] = v[1]
      temp['count'] = v[0]
      v_temp.append(temp)
      temp = {}
   ventas_sw_cliente = v_temp

   return render(request, 'reporte.html', {'ventas_sw_cliente':ventas_sw_cliente,'clientes':clientes,'ventas_cliente':ventas_cliente,'ventas_ingrediente': ventas_ingrediente,'ventas_size': ventas_size, 'ventas_totales': ventas_totales, 'ventas_sw_totales': ventas_sw_totales, 'ventas_dia': ventas_dia, 'ventas_sw_dia':ventas_sw_dia})
   

'''
def verVentrasDia(request):
   context = []
   vista = {}

   ventas = vetanrealizada.objects.filter(fecha=date.today())
   
   for v in ventas: 
      vista['venta_id'] = v.venta_id
      fecha = v.fecha
      vista['venta_fecha'] = fecha.strftime("%d-%m-%Y")
      vista['venta_total'] = v.total
      vista['venta_deli'] = v.delivery
      vista['venta_pago'] = v.metodo_pago
      vista['cliente'] = v.cliente_id.identificacion
      vista['cliente_nombre'] = v.cliente_id.nombre + ' ' + v.cliente_id.apellido
      vista['cliente_direccion'] = v.cliente_id.direccion
      
      ordenes = []
      sandwiches = emparerado.objects.filter(venta_id=v.venta_id)
      for s in sandwiches:
         orden = {}
         sw = s.sandwich_id
         orden['size'] = s.dimension_id.nombre
         ingrediente = []
         contenido = tablacontenido.objects.filter(sandwich_id=s.sandwich_id)
         for c in contenido:
            ingrediente.append(c.ingrediente_id.nombre)
            orden['ingrediente'] = ingrediente
         ordenes.append(orden)
      vista['ordenes'] = ordenes
      context.append(vista)
      vista={}
      
   return render(request, 'test.html', {'context': context})

def verVentrasSandwich(request):
   context = []
   vista = {}

   sandwich = emparerado.objects.filter(dimension_id=3)
   for s in sandwich:
      vista['venta_id'] = s.venta_id.venta_id
      fecha = s.venta_id.fecha
      vista['venta_fecha'] = fecha.strftime("%d-%m-%Y")
      vista['venta_total'] = s.venta_id.total
      vista['venta_deli'] = s.venta_id.delivery
      vista['venta_pago'] = s.venta_id.metodo_pago
      vista['cliente'] = s.venta_id.cliente_id.identificacion
      vista['cliente_nombre'] = s.venta_id.cliente_id.nombre + ' ' + s.venta_id.cliente_id.apellido
      vista['cliente_direccion'] = s.venta_id.cliente_id.direccion
      
      ordenes = []
      sandwiches = emparerado.objects.filter(venta_id=s.venta_id.venta_id)
      for s in sandwiches:
         orden = {}
         sw = s.sandwich_id
         orden['size'] = s.dimension_id.nombre
         ingrediente = []
         contenido = tablacontenido.objects.filter(sandwich_id=s.sandwich_id)
         for c in contenido:
            ingrediente.append(c.ingrediente_id.nombre)
            orden['ingrediente'] = ingrediente
         ordenes.append(orden)
      vista['ordenes'] = ordenes
      context.append(vista)
      vista={}
   
   venta=[]
   fix=[]
   for c in context:
      if c['venta_id'] not in venta:
         venta.append(c['venta_id'])
         fix.append(c)
   context = fix

   return render(request, 'test.html', {'context': context})

def verVentrasIngrediente(request):
   context = []
   vista = {}

   contenido = tablacontenido.objects.filter(ingrediente_id=1)

   for c in contenido:
      vista['venta_id'] = c.sandwich_id.venta_id.venta_id
      fecha = c.sandwich_id.venta_id.fecha
      vista['venta_fecha'] = fecha.strftime("%d-%m-%Y")
      vista['venta_total'] = c.sandwich_id.venta_id.total
      vista['venta_deli'] = c.sandwich_id.venta_id.delivery
      vista['venta_pago'] = c.sandwich_id.venta_id.metodo_pago
      vista['cliente'] = c.sandwich_id.venta_id.cliente_id.identificacion
      vista['cliente_nombre'] = c.sandwich_id.venta_id.cliente_id.nombre + ' ' + c.sandwich_id.venta_id.cliente_id.apellido
      vista['cliente_direccion'] = c.sandwich_id.venta_id.cliente_id.direccion
      
      ordenes = []
      sandwiches = emparerado.objects.filter(venta_id=c.sandwich_id.venta_id.venta_id)
      for s in sandwiches:
         orden = {}
         sw = s.sandwich_id
         orden['size'] = s.dimension_id.nombre
         ingrediente = []
         contenido = tablacontenido.objects.filter(sandwich_id=s.sandwich_id)
         for c in contenido:
            ingrediente.append(c.ingrediente_id.nombre)
            orden['ingrediente'] = ingrediente
         ordenes.append(orden)
      vista['ordenes'] = ordenes
      context.append(vista)
      vista={}
   
   venta=[]
   fix=[]
   for c in context:
      if c['venta_id'] not in venta:
         venta.append(c['venta_id'])
         fix.append(c)
   context = fix

   return render(request, 'test.html', {'context': context})

def verVentasClientes(request):
   pass
'''