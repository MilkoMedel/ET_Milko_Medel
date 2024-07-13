# web/carrito_prod.py

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_prod = self.session.get("carrito_prod")
        if not carrito_prod:
            carrito_prod = self.session["carrito_prod"] = {}
        self.carrito_prod = carrito_prod 

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito_prod.keys():
            self.carrito_prod[id] = {
                "id": producto.id,
                "nombre": producto.nombre,
                "description": producto.description,
                "precio": str(producto.precio),
                "cantidad": 1,
                "total": producto.precio,
                "url": producto.imagen.url,
            }
        else:
            self.carrito_prod[id]['cantidad'] = self.carrito_prod[id]['cantidad'] + 1
            self.carrito_prod[id]['precio'] = producto.precio
            self.carrito_prod[id]['total'] = self.carrito_prod[id]['total'] + producto.precio
        self.guardar_carrito()

    def get_amount(self, producto):
        id = str(producto.id)
        try:
            return self.carrito_prod[id]['cantidad']
        except:
            return 0

    def guardar_carrito(self):
        self.session["carrito_prod"] = self.carrito_prod
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito_prod: 
            del self.carrito_prod[id]
            self.guardar_carrito()

    def restar(self, producto):
        for key, value in self.carrito_prod.items():
            if key == str(producto.id):
                value['cantidad'] = value['cantidad'] - 1
                value['total'] = value['total'] - producto.precio
                if value['cantidad'] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carrito()

    def limpiar(self):
        self.session["carrito_prod_open"] = False
        self.session["carrito_prod"] = {}
        self.session.modified = True 

    def obtener_total(self):
        total = 0
        for key, value in self.carrito_prod.items():
            total += int(value['total'])
        return total
