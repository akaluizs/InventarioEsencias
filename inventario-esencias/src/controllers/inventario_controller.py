class InventarioController:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def agregar_producto(self, id, nombre, stock_actual, stock_minimo, proveedor, fecha_caducidad, costo_por_ml):
        producto = self.modelo.Producto(id, nombre, stock_actual, stock_minimo, proveedor, fecha_caducidad, costo_por_ml)
        self.modelo.agregar_producto(producto)
        self.vista.actualizar_tabla(self.modelo.obtener_productos())

    def eliminar_producto(self, id):
        self.modelo.eliminar_producto(id)
        self.vista.actualizar_tabla(self.modelo.obtener_productos())

    def actualizar_producto(self, id, nombre, stock_actual, stock_minimo, proveedor, fecha_caducidad, costo_por_ml):
        producto = self.modelo.Producto(id, nombre, stock_actual, stock_minimo, proveedor, fecha_caducidad, costo_por_ml)
        self.modelo.actualizar_producto(producto)
        self.vista.actualizar_tabla(self.modelo.obtener_productos())

    def cargar_productos(self):
        productos = self.modelo.cargar_productos()
        self.vista.mostrar_productos(productos)