from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.timezone import now 
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
    id_producto     = models.CharField(max_length=100, primary_key=True)
    nombre          = models.CharField(max_length=100)
    description     = models.CharField(max_length=500)
    precio          = models.IntegerField()
    stock           = models.IntegerField()
    imagen          = models.ImageField()
    categoria       = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    id          = models.AutoField(primary_key=True)
    total       = models.BigIntegerField()
    impuesto    = models.BigIntegerField(default=0)
    estado      = models.IntegerField(default=3)
    valor_envio = models.BigIntegerField(default=0)
    date        = models.DateTimeField(blank=False, null=False, default=now)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def estado_str(self):
        if self.estado == 0:
            return 'Procesando servicios'
        if self.estado == 1:
            return 'Servicios confirmados y en espera del dia'
        if self.estado == 2:
            return 'Servicios recibidos'
        return 'Desconocido'
    
    def __str__(self):
        return str(self.id)
    
    @property
    def barra_estado(self):
        return round(self.estado * 33.3)
        
class Detalles_Pedido(models.Model):
    id          = models.AutoField(primary_key=True)
    order_id    = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles_pedido')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    monto       = models.IntegerField()
    sub_total   = models.IntegerField()
