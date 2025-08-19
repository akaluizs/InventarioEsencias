class Salida:
    def __init__(self, id_salida, id_producto, cantidad_vendida, precio_venta, fecha_venta, cliente=None):
        self.id_salida = id_salida
        self.id_producto = id_producto
        self.cantidad_vendida = cantidad_vendida
        self.precio_venta = precio_venta
        self.fecha_venta = fecha_venta
        self.cliente = cliente

    def calcular_ganancia(self, costo_entrada, cantidad_total_producto):
        """
        Calcula la ganancia de la venta
        
        Args:
            costo_entrada: Costo total de entrada del producto
            cantidad_total_producto: Cantidad total que se compró del producto
            
        Returns:
            float: Ganancia obtenida
        """
        costo_por_ml = costo_entrada / cantidad_total_producto if cantidad_total_producto > 0 else 0
        costo_total_vendido = costo_por_ml * self.cantidad_vendida
        ganancia = self.precio_venta - costo_total_vendido
        return ganancia

    def calcular_total_venta(self):
        """Calcula el total de la venta"""
        return self.precio_venta
