from django.db import connection
from .forms import FormCliente
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Cliente as comprador, Venta as vetanrealizada, Sandwich as emparerado

def addCliente(request):
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
            ingredientes.append('Jamón')
            precio=precio+40
         elif parte == 'cha':
            ingredientes.append('Champiñones')
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
            ingredientes.append('Pimentón')
            precio=precio+30
         elif parte == 'sal':
            ingredientes.append('Salchichón')
            precio=precio+62.5
            
      sandwich['precio'] = precio
      sandwich['ingrediente'] = ingredientes
      n=n+1
      sandwiches.append(sandwich)
      total = total+precio

   return sandwiches, total

def finalizarVenta(request):
   cliente = request.session['cliente']
   sandwiches, precio = traducir(request, request.session['sandwiches'])
   if request.method == 'POST':
      deli = request.POST['deli']
      metodo = request.POST['metodo']

      try:
         test = comprador.objects.get(identificacion=int(cliente['i']))
      except comprador.DoesNotExist:
         guardar_cliente(request, cliente)

      guardar_venta(request, deli, metodo, int(precio), int(cliente['i']))

      guardar_sandwiches(request, sandwiches)

      return redirect('cliente')

   return render(request, 'finalizar_venta.html', {'cliente':cliente, 'sandwiches':sandwiches, 'precio':precio})

def guardar_cliente(request, cliente):
   with connection.cursor() as cursor:
        cursor.execute (
         "INSERT INTO user_cliente(nombre, apellido, direccion, identificacion) VALUES (%s, %s, %s, %s);",
        [cliente['n'], cliente['a'], cliente['d'], int(cliente['i'])])

def guardar_venta(request, deli, metodo, precio, cliente):
   id = comprador.objects.get(identificacion=cliente)
   with connection.cursor() as cursor:
        cursor.execute (
         "INSERT INTO user_venta(cliente_id_id, fecha, total, delivery, metodo_pago) VALUES (%s, date('now'), %s, %s, %s);",
        [id.cliente_id, precio, deli, metodo])

def guardar_sandwiches(request, sandwiches):
   venta = vetanrealizada.objects.last()
   venta = venta.venta_id
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
