class Producto:
    # Constantes para géneros
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"
    UNISEX = "Unisex"
    
    GENEROS_DISPONIBLES = [MASCULINO, FEMENINO, UNISEX]
    
    def __init__(self, id_producto, nombre, stock_actual, costo_entrada, proveedor, fecha_caducidad, costo_por_ml, genero=UNISEX):
        self.id_producto = id_producto
        self.nombre = nombre
        self.stock_actual = stock_actual
        self.costo_entrada = costo_entrada
        self.proveedor = proveedor
        self.fecha_caducidad = fecha_caducidad
        self.costo_por_ml = costo_por_ml
        
        # Validar género
        if genero not in self.GENEROS_DISPONIBLES:
            raise ValueError(f"Género '{genero}' no válido. Debe ser uno de: {', '.join(self.GENEROS_DISPONIBLES)}")
        
        self.genero = genero

    def valor_total_stock(self):
        return self.stock_actual * self.costo_por_ml

    def stock_bajo(self):
        """Verifica si el stock está bajo (menos de 50ml)"""
        return self.stock_actual < 50

    def get_icono_genero(self):
        """Retorna un emoji representativo del género"""
        iconos = {
            self.MASCULINO: "♂️",
            self.FEMENINO: "♀️", 
            self.UNISEX: "⚧️"
        }
        return iconos.get(self.genero, "❓")
    
    def get_color_genero(self):
        """Retorna un color representativo del género para la UI"""
        colores = {
            self.MASCULINO: "#1976D2",  # Azul
            self.FEMENINO: "#E91E63",   # Rosa
            self.UNISEX: "#9C27B0"      # Púrpura
        }
        return colores.get(self.genero, "#757575")