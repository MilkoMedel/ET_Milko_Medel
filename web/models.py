from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Genero(models.Model):
    id_genero       = models.AutoField(db_column='idGenero', primary_key=True)
    genero          = models.CharField(max_length=20, blank=False, null=False)
    
    def __str__(self):
        return str(self.genero)

class Registro_cliente(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE) # username y contrasena
    fecha_nac   = models.DateField()
    id_genero   = models.ForeignKey('Genero', on_delete=models.CASCADE, db_column='idGenero')
    cel         = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Categoria(models.Model):
    id_categoria        = models.IntegerField(primary_key=True, verbose_name="Id de categoria")
    nombreCategoria     = models.CharField(max_length=50, blank=True, verbose_name="Nombre de categoria")
    
    def __str__(self):
        return self.nombreCategoria
    
class Producto(models.Model):
    id_producto     = models.AutoField(max_length=100, primary_key=True)
    nombre          = models.CharField(max_length=100)
    description     = models.CharField(max_length=500)
    precio          = models.IntegerField()
    stock           = models.IntegerField()
    imagen          = models.ImageField()
    categoria       = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    
    def __str__(self):
        return self.get_code_id

    def get_code_id(self):
        return f"{self.id_producto} - {self.nombre}"


