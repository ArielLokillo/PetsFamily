from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import *
import requests 
# Create your views here.

class ProductoViewset(viewsets.ModelViewSet):
	queryset = Producto.objects.all()
	#queryset = Producto.objects.filter(tipo=1)
	serializer_class = ProductoSerializer
	
    
def indexapi(request):
	#REALIZAMOS LA SOLICITUD AL API
	respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
	respuesta2 = requests.get('https://mindicador.cl/api')
	respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
	# TRANSFORMAMOS EL JSON
	productos = respuesta.json()
	monedas = respuesta2.json()
	aux = respuesta3.json()
	personajes = aux['results']

	data = {
		'listaProductos': productos,
		'monedas': monedas,
		'personajes': personajes,
	}
	return render(request, 'core/indexapi.html', data)

def index(request):
	productosAll = Producto.objects.all()
	page = request.GET.get('page', 1)
	try:
		paginator = Paginator(productosAll, 8)
		productosAll = paginator.page(page)
	except:
	    raise Http404

	data = {
		'listaProductos': productosAll,
		'paginator': paginator
	}
	return render(request, 'core/index.html', data)

def blog(request):
	return render(request, 'core/blog.html')

#def cart(request):
    
   #carro_compras = CarroCompras.objects.get(usuario=request.user)
   #tems = carro_compras.items.all()
   #otal = carro_compras.total()

   #ata = {
   #   'items': items,
   #   'total': total,
   #

   #eturn render(request,'core/cart.html',data)
def cart(request):
	
	# LOGICA DEL CARRITO, SE SUMAN TODOS LOS PRECIOS
    carro_compras = CarroCompras.objects.get(usuario=request.user)
    items = carro_compras.items.all()
    total = carro_compras.total()
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    valor_carrito = 'total' #SE SUPONE QUE ES EL TOTAL DEL CARRITO
    valor_total = total/valor_usd

    data = {
		'total': round(valor_total,2),
	    'items': items,
        
	}
    return render(request, 'core/cart.html',data)


def cartUser(request):
	return render(request, 'core/cartUser.html')

def category(request):
	productosAll = Producto.objects.all()
	data = {
		'listaProductos' : productosAll
	}
	return render(request, 'core/category.html', data)	
		
def checkout(request):
	return render(request, 'core/checkout.html')		
						
def confirmation(request):
	return render(request, 'core/confirmation.html')

def contact(request):
	return render(request, 'core/contact.html')
		
def indexUser(request):
	return render(request, 'core/indexUser.html')				
						
def indexUserSubscito(request):
	return render(request, 'core/indexUserSubscito.html')	

def login(request):
	return render(request, 'core/login.html')
		
def perfil(request):
	return render(request, 'core/perfil.html')	

def register(request):
	return render(request, 'core/register.html')

def singleblog(request):
	return render(request, 'core/single-blog.html')

def singleproduct(request):
	return render(request, 'core/single-product.html')

def subsForm(request):
	return render(request, 'core/subsForm.html')

def trackingorder(request):
	return render(request, 'core/tracking-order.html')


#crud
@permission_required('app.add')
def add(request):
	data = {
		'form': ProductoForm()
	}
	if request.method == 'POST':
		formulario = ProductoForm(request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			#data['msj'] = "Producto almacenado correctamente"
			messages.success(request, "Producto almacenado correctamente")

	return render(request, 'core/add-product.html', data)
@permission_required('app.update/<id>/')
def update(request,id):
	producto = Producto.objects.get(id=id)
	data = {
		'form': ProductoForm(instance=producto)
	}
	if request.method == 'POST':
		formulario = ProductoForm(data=request.POST, instance=producto)
		if formulario.is_valid():
			formulario.save()
			#data['msj'] = "Producto actualizado correctamente"
			messages.success(request, "Producto actualizado correctamente")
			data['form'] = formulario

	return render(request, 'core/update-product.html', data)
@permission_required('app.delete/<id>/')
def delete(request,id):
    producto = Producto.objects.get(id=id); # OBTENEMOS UN PRODUCTO
    producto.delete()

    return redirect(to="index")


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
        if user is created:
            assign_user_to_group('usuario')
        user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
        login(request, user)
        messages.success(request, "Te has registrado correctamente")
            #redirigir al home
        return redirect(to="core/index")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)





def checkout(request):
    
    carro_compras = CarroCompras.objects.get(usuario=request.user)
    items = carro_compras.items.all()
    total = carro_compras.total()
    
    total_productos = 0
    for item in items:
        total_productos += item.producto.precio * item.cantidad

    valor_fijo = 7560

    total_final = total_productos + valor_fijo

    data = {
        'items': items,
        'total': total,
        'total_final' : total_final
    }

    if request.method == 'POST':
        compra = Compra.objects.create(usuario=request.user)
        for item in items:
            CompraItem.objects.create(compra=compra, carro_item=item)

        carro_compras.compra = compra
        carro_compras.save()
        
        return render(request, 'core/confirmation.html', data)

    return render(request,'core/checkout.html',data)

def confirmation(request):

    carro_compras = CarroCompras.objects.get(usuario=request.user)
    items = carro_compras.items.all()
    total = carro_compras.total()
    


    total_productos = 0
    for item in items:
        total_productos += item.producto.precio * item.cantidad

    valor_fijo = 7560

    total_final = total_productos + valor_fijo

    data = {
        'items': items,
        'total': total,
        'total_final' : total_final
    }

    return render(request,'core/confirmation.html',data)

def cartadd(request,id):
    producto = Producto.objects.get(id=id)
    carro_compras, created = CarroCompras.objects.get_or_create(usuario=request.user)
    carro_item, item_created = CarroItem.objects.get_or_create(producto=producto, usuario=request.user)
    if not item_created:
        carro_item.cantidad +=1
        carro_item.save()

    carro_compras.items.add(carro_item)
    carro_compras.save()

    return redirect(to='cart')

def cartdel(request,id):
    producto = Producto.objects.get(id=id)
    carro_compras = CarroCompras.objects.get(usuario = request.user)
    carro_item = carro_compras.items.get(producto=producto)
    if carro_item.cantidad > 1:
        carro_item.cantidad -= 1
        carro_item.save()
    else:
        carro_compras.items.remove(carro_item)
        carro_item.delete()
 
    return redirect(to='cart')

def cartdelete(request,id):
    producto = Producto.objects.get(id=id)
    carro_compras = CarroCompras.objects.get(usuario = request.user)
    carro_item = carro_compras.items.get(producto=producto)

    carro_compras.items.remove(carro_item)
    carro_item.delete()
    return redirect(to='cart')

def add_compra(request): 
    carro_compras = CarroCompras.objects.get(usuario = request.user)
    items = carro_compras.items.all()

    compra = Compra.objects.create(usuario = request.user)
    for item in items:
        CompraItem.objects.create(compra = compra, carro_item = item)

    carro_compras.items.clear()
    return redirect(to='confirmation')





