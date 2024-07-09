class Carrito_Prod:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito_producto = self.session.get('carrito_producto')
        if not carrito_producto:
            carrito_producto = self.session['carrito_producto'] = {}
        self.carrito_producto = carrito_producto

    def add(self, producto):
        id = str(producto.id_producto)
        if id not in self.carrito_producto.keys():
            self.carrito_producto[id]={
                'id': producto.id_producto,
                'nombre': producto.nombre,
                'description': producto.description,
                'precio': str(producto.precio),
                'cantidad': 1,
                'total': producto.total,
                'url': producto.imagen.url,
            }
        else:
            self.carrito_producto[id]['cantidad'] = self.carrito_producto[id]['cantidad'] + 1
            self.carrito_producto[id]['precio'] = producto.precio
            self.carrito_producto[id]['total'] = self.carrito_producto[id]['total'] + producto.precio
        self.save()
    
    def get_amount(self, producto):
        id = str(producto.id_producto)
        try:
            return self.carrito_producto[id]['cantidad']
        except:
            return 0
        
    def save(self):
        self.session['carrito_producto'] = self.carrito_producto
        self.session.modified = True

    def delete(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito_producto:
            del self.carrito_producto[id]
            self.save()
    
    def substract(self, producto):
        for key, value in self.carrito_producto.items():
            if key == str(producto.id_producto):
                value['cantidad'] = value['cantidad'] - 1
                value['total'] = value['total'] - producto.precio
                if value['cantidad'] < 1:
                    self.delete(producto)
                break
        self.save()

    def clear(self):
        self.session['carrito_abierto'] = False
        self.session['carrito_producto'] = {}
        self.session.modified = True