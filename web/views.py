from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .forms import SignUpForm, CustomAuthenticationForm, ProductosForm
from .models import Registro_cliente, Producto,Categoria

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def nosotros(request):
    return render(request,'nosotros.html')

@login_required
def galeria(request):
    products = Producto.objects.all()
    ctx = {
        'products': products 
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
    product = get_object_or_404(Producto, id_producto=id)
    ctx = {
        'form': ProductosForm(instance=product),
        'id_producto': id,
    }
    if request.method == "POST":
        form = ProductosForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('crud')
    return render(request, 'producto/producto_mod.html', ctx)

@staff_member_required
def producto_del(request, id):
    product = get_object_or_404(Producto, id_producto=id)
    product.delete()
    return redirect('crud')