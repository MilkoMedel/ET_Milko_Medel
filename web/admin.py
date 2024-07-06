from django.contrib import admin
from .models import Genero, Registro_cliente,Categoria,Producto

# Register your models here.

admin.site.register(Genero)
admin.site.register(Registro_cliente)
admin.site.register(Categoria)
admin.site.register(Producto)