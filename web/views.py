from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

from web.carrito_prod import Carrito
from web.context_processor import calculate_shipping, calculate_taxes, get_page_number
from .forms import SignUpForm, CustomAuthenticationForm, ProductosForm, UserProfileForm
from .models import Detalles_Pedido, Pedido, Registro_cliente, Producto,Categoria

#           vistas de la pagina

def index(request):
    return render(request, 'index.html')

@login_required
def nosotros(request):
    return render(request,'nosotros.html')

@login_required
def galeria(request):
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')

    products = Producto.objects.all()

    if search_query:
        products = products.filter(Q(nombre__icontains=search_query) | Q(description__icontains=search_query))

    if category_query:
        products = products.filter(categoria__nombreCategoria=category_query)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    ctx = {
        'page_obj': page_obj,
        'products': products,  # Pasa también los productos sin paginar
        'categorias': categorias,
    }
    return render(request, 'galeria.html', ctx)

def form(request):
    data = {
        'form': SignUpForm()
    }
    if request.method == "POST":
        formulario = SignUpForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            genero = formulario.cleaned_data.get('genero')
            fecha_nac = formulario.cleaned_data.get('fecha_nac')
            cel = formulario.cleaned_data.get('cel')
            Registro_cliente.objects.create(user=user, id_genero=genero, fecha_nac=fecha_nac, cel=cel)
            
            # Authenticate and log in the user
            username = formulario.cleaned_data.get('username')
            password = formulario.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Te has registrado correctamente")
                return redirect('index')
            else:
                messages.error(request, "Hubo un problema con la autenticación")
        
        data["form"] = formulario
    
    return render(request, 'registration/form.html', data)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to a home page or any other page
            else:
                return HttpResponse("Invalid login")
        else:
            return HttpResponse("Invalid form")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})    # inicia sesion.

#           CRUD de productos admin

def crud(request):
    products = Producto.objects.all()
    ctx = {
        'products': products 
    }
    return render(request, 'producto/crud.html', ctx)         # cambia a la lista de productos para mod,add,del

def producto(request):
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')

    products = Producto.objects.all()

    if search_query:
        products = products.filter(Q(nombre__icontains=search_query) | Q(description__icontains=search_query))

    if category_query:
        products = products.filter(categoria__nombreCategoria=category_query)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    ctx = {
        'page_obj': page_obj,
        'products': products,  # Pasa también los productos sin paginar
        'categorias': categorias,
    }
    return render(request, 'galeria.html', ctx)

@staff_member_required
def producto_add(request):
    if request.method == "POST":
        form = ProductosForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crud')
    else:
        form = ProductosForm()
    return render(request, 'producto/producto_add.html', {'form': form})

@staff_member_required
def producto_mod(request, id):
    product = get_object_or_404(Producto, id=id)
    ctx = {
        'form': ProductosForm(instance=product),
        'id': id,
    }
    if request.method == "POST":
        form = ProductosForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('crud')
    return render(request, 'producto/producto_mod.html', ctx)

@staff_member_required
def producto_del(request, id):
    product = get_object_or_404(Producto, id=id)
    product.delete()
    return redirect('crud')

#           Perfil del usuario

@login_required
def perfil(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            registro_cliente = Registro_cliente.objects.get(user=user)
            registro_cliente.fecha_nac = form.cleaned_data['fecha_nac']
            registro_cliente.id_genero = form.cleaned_data['genero']
            registro_cliente.cel = form.cleaned_data['cel']
            registro_cliente.save()
            return redirect('mostrar_perfil')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'usuario/perfil.html', {'form': form})

@login_required
def mostrar_perfil(request):
    user = request.user
    return render(request, 'usuario/mostrar_perfil.html', {'user': user})

#           carrito de compras 

@login_required
def mostrar_carrito(request):
    carrito_compra = Carrito(request)
    context = {
        'carrito': carrito_compra.carrito_prod,
        'total': carrito_compra.obtener_total(),
    }
    return render(request, 'producto/carrito.html', context)

@login_required
def carrito_prod_open(request):
    page = get_page_number(request)
    request.session['carrito_prod_open'] = True
    return redirect(reverse('galeria') + '?page=' + str(page))

@login_required
def carrito_prod_close(request):
    page = get_page_number(request)
    request.session['carrito_prod_open'] = False
    return redirect(reverse('galeria') + '?page=' + str(page))

@login_required
def agregar_producto(request, id):
    page = request.GET.get('page', 1)
    carrito_compra = Carrito(request)
    producto = get_object_or_404(Producto, id=id)
    
    # Verificar el stock antes de agregar el producto
    if producto.stock - carrito_compra.get_amount(producto) <= 0:
        return redirect(reverse('producto') + '?page=' + str(page))
    
    carrito_compra.agregar(producto)
    return redirect('mostrar_carrito')
    

@login_required
def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('mostrar_carrito')

@login_required
def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito_compra.restar(producto=producto)
    return redirect('mostrar_carrito')

@login_required
def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect(reverse('carrito')) 


#               Boletas

@login_required
def create_order(request):
    carrito_compra = Carrito(request)
    total = carrito_compra.obtener_total()

    if total <= 0:
        return redirect('producto')
    
    estado = calculate_shipping(total)
    impuesto = calculate_taxes(total)
    
    orden = Pedido(user=request.user, total=total + estado + impuesto, estado=estado, impuesto=impuesto)
    orden.save()
    
    products = []
    for key, value in carrito_compra.carrito_prod.items():
        product = Producto.objects.get(id=key)
        cantidad = int(value['cantidad'])
        
        if product.stock < cantidad:
            continue
        
        product.stock -= cantidad
        product.save()
        
        subtotal = cantidad * product.precio
        detail = Detalles_Pedido(order_id=orden, id_producto=product, monto=cantidad, sub_total=subtotal)
        detail.save()
        
        products.append(detail)
    
    carrito_compra.limpiar()
    
    ctx = {
        'products': products,
        'date': orden.date,
        'total': orden.total,
        'estado': estado,
        'impuesto': impuesto,
    }

    return render(request, 'producto/detalle_boleta.html', ctx)



