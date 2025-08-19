class Producto:
    def __init__(self, id_producto, nombre, stock_actual, costo_entrada, proveedor, fecha_caducidad, costo_por_ml):
        self.id_producto = id_producto
        self.nombre = nombre
        self.stock_actual = stock_actual
        self.costo_entrada = costo_entrada
        self.proveedor = proveedor
        self.fecha_caducidad = fecha_caducidad
        self.costo_por_ml = costo_por_ml

    def valor_total_stock(self):
        return self.stock_actual * self.costo_por_ml

    def necesita_reabastecimiento(self):
        return self.stock_actual < 50  # Umbral fijo de 50ml para reabastecimiento