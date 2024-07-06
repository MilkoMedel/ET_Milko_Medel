from django import forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from .models import Genero,Producto,Registro_cliente,Categoria

class SignUpForm(UserCreationForm):
    genero      = forms.ModelChoiceField(Genero.objects.all(),required=True,label="Genero")
    fecha_nac   = forms.DateField()
    cel         = forms.IntegerField()
    class Meta:
        model=User
        fields = ['username', 
                'password1', 
                'password2', 
                'email', 
                'genero', 
                'fecha_nac',
                'cel']
    pass

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['id_producto',
                'nombre', 
                'description', 
                'precio', 
                'stock', 
                'imagen',
                'categoria']
        labels ={
            'id_producto' : 'ID',
            'nombre' : 'Nombre',
            'description': 'Descripción',
            'precio': 'Precio',
            'stock': 'Stock',
            'imagen': 'Imagen',
            'categoria':'Categoria',
        }
        widgets = {
            'id_producto': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese id...',
                    'id': 'id',
                    'class': 'form-control',
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre...',
                    'id': 'nombre',
                    'class': 'form-control',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese descripción...',
                    'id': 'description',
                    'class': 'form-control',
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese precio...',
                    'id': 'precio',
                    'class': 'form-control',
                }
            ),
            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'stock',
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'imagen',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'id':'categoria',
                    'class':'form-control',
                }
            )
        }
