from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms  import UserCreationForm,AuthenticationForm
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
        fields = ['id',
                'nombre', 
                'description', 
                'precio', 
                'stock', 
                'imagen',
                'categoria']
        labels ={
            'id' : 'ID',
            'nombre' : 'Nombre',
            'description': 'Descripción',
            'precio': 'Precio',
            'stock': 'Stock',
            'imagen': 'Imagen',
            'categoria':'Categoria',
        }
        widgets = {
            'id': forms.TextInput(
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

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Ingresar', css_class='btn btn-success'))

class UserProfileForm(forms.ModelForm):
    genero = forms.ModelChoiceField(Genero.objects.all(), required=True, label="Género")
    fecha_nac = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'text', 
            'placeholder': 'Ejemplo: 1985-10-10',
            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
            'title': 'Se ingresa como AÑO-MES-DIA'
        }),
        input_formats=['%Y-%m-%d']
    )
    cel = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'genero', 'fecha_nac', 'cel']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'registro_cliente'):
            self.fields['fecha_nac'].initial = self.instance.registro_cliente.fecha_nac
            self.fields['genero'].initial = self.instance.registro_cliente.id_genero
            self.fields['cel'].initial = self.instance.registro_cliente.cel

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            registro_cliente, created = Registro_cliente.objects.get_or_create(user=user)
            registro_cliente.fecha_nac = self.cleaned_data['fecha_nac']
            registro_cliente.id_genero = self.cleaned_data['genero']
            registro_cliente.cel = self.cleaned_data['cel']
            registro_cliente.save()
        return user
