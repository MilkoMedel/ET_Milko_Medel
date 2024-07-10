#  imports
from web.models import Producto

# metodos de la clase C arrito
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_prod = self.session.get("carrito_prod")
        if not carrito_prod:
            carrito_prod = self.session["carrito_prod"] = {}
        self.carrito_prod=carrito_prod 
    
    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito_prod.keys():
            self.carrito_prod[id]={
                "id":producto.id, 
                "nombre": producto.nombre,
                "description": producto.description,
                "precio": str (producto.precio),
                "cantidad": 1,
                "total": producto.precio,
                "url": producto.imagen.url,
            }
        else:
            for key, value in self.carrito_prod.items():
                if key==producto.id:
                    value["cantidad"] = value["cantidad"]+1
                    value["precio"] = producto.precio
                    value["total"]= value["total"] + producto.precio
                    break
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito_prod"] = self.carrito_prod
        self.session.modified=True


    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito_prod: 
            del self.carrito_prod[id]
            self.guardar_carrito()
    
    def restar (self,producto):
        for key, value in self.carrito_prod.items():
            if key == producto.id:
                value["cantidad"] = value["cantidad"]-1
                value["total"] = int(value["total"])- producto.precio
                if value["cantidad"] < 1:   
                    self.eliminar(producto)
                break
        self.guardar_carrito()
    
    def limpiar(self):
        self.session["carrito_prod_open"] = False
        self.session["carrito_prod"]={}
        self.session.modified=True 
