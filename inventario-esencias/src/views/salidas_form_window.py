import flet as ft
from datetime import datetime
from utils.alerts import AlertManager

class DarkTheme:
    # Colores de fondo
    PRIMARY_BG = ft.Colors.GREY_900
    SECONDARY_BG = ft.Colors.GREY_800
    CARD_BG = ft.Colors.GREY_700
    SURFACE_BG = ft.Colors.GREY_600
    
    # Colores de texto
    PRIMARY_TEXT = ft.Colors.WHITE
    SECONDARY_TEXT = ft.Colors.GREY_300
    MUTED_TEXT = ft.Colors.GREY_400
    
    # Colores de estado
    SUCCESS = ft.Colors.GREEN_400
    ERROR = ft.Colors.RED_400
    WARNING = ft.Colors.ORANGE_400
    INFO = ft.Colors.BLUE_400
    
    # Colores de botones
    BUTTON_PRIMARY = ft.Colors.BLUE_600
    BUTTON_SUCCESS = ft.Colors.GREEN_600
    BUTTON_DANGER = ft.Colors.RED_600
    BUTTON_SECONDARY = ft.Colors.GREY_600
    
    # Otros
    ACCENT = ft.Colors.CYAN_400
    BORDER_COLOR = ft.Colors.GREY_600
    DIVIDER_COLOR = ft.Colors.GREY_600

class SalidasFormWindow:
    def __init__(self, page, productos_disponibles=None):
        self.page = page
        self.productos_disponibles = productos_disponibles or []
        
        # Sistema de alertas
        self.alert_manager = AlertManager(page)
        
        # Callbacks
        self.on_save = None
        self.on_cancel = None
        
        # Guardar el contenido original de la página
        self.original_content = None
        
        # Campos del formulario
        self._crear_campos()
        self._crear_formulario()
    
    def _crear_campos(self):
        """Crea los campos del formulario"""
        # Dropdown para seleccionar producto
        self.producto_dropdown = ft.Dropdown(
            label="Seleccionar Producto",
            width=400,
            options=[
                ft.dropdown.Option(
                    key=producto['id_producto'],
                    text=f"{producto['nombre']} - Stock: {producto['stock_actual']} ml"
                ) 
                for producto in self.productos_disponibles
            ],
            on_change=self._on_producto_changed
        )
        
        # Campo para mostrar información del producto seleccionado
        self.info_producto = ft.Container(
            content=ft.Text("Selecciona un producto para ver la información", 
                          color=DarkTheme.MUTED_TEXT, size=14),
            padding=10,
            bgcolor=DarkTheme.SURFACE_BG,
            border_radius=8,
            visible=True
        )
        
        # Campos de venta
        self.cantidad_field = ft.TextField(
            label="Cantidad a vender (ml)",
            width=200,
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._calcular_total
        )
        
        self.precio_unitario_field = ft.TextField(
            label="Precio por ml (Q)",
            width=200,
            value="0.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._calcular_total
        )
        
        self.cliente_field = ft.TextField(
            label="Cliente (opcional)",
            width=300,
            value=""
        )
        
        # Campos calculados (solo lectura)
        self.total_venta_text = ft.Text(
            "Total: Q0.00",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=DarkTheme.SUCCESS
        )
        
        self.ganancia_estimada_text = ft.Text(
            "Ganancia estimada: Q0.00",
            size=16,
            color=DarkTheme.INFO
        )
    
    def _crear_formulario(self):
        """Crea el contenido del formulario para ventana completa"""
        # Encabezado principal
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=DarkTheme.PRIMARY_TEXT,
                    on_click=self._cerrar_formulario,
                    tooltip="Volver"
                ),
                ft.Icon(ft.Icons.POINT_OF_SALE, size=40, color=DarkTheme.SUCCESS),
                ft.Text(
                    "Registrar Venta",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=DarkTheme.PRIMARY_TEXT
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.START),
            padding=ft.Padding(30, 20, 30, 20),
            bgcolor=DarkTheme.PRIMARY_BG,
            border_radius=ft.border_radius.only(top_left=15, top_right=15)
        )
        
        # Contenido del formulario
        form_content = ft.Container(
            content=ft.Column([
                # Selección de producto
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.INVENTORY_2, color=DarkTheme.INFO, size=24),
                            ft.Text("Selección de Producto", size=20, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ], spacing=10),
                        ft.Divider(color=DarkTheme.DIVIDER_COLOR, height=20),
                        self.producto_dropdown,
                        self.info_producto,
                    ], spacing=15),
                    padding=ft.Padding(25, 20, 25, 20),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                    border_radius=12,
                    bgcolor=DarkTheme.CARD_BG,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Detalles de venta
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SHOPPING_CART, color=DarkTheme.WARNING, size=24),
                            ft.Text("Detalles de Venta", size=20, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ], spacing=10),
                        ft.Divider(color=DarkTheme.DIVIDER_COLOR, height=20),
                        ft.Row([
                            self.cantidad_field,
                            self.precio_unitario_field,
                        ], wrap=True, spacing=20),
                        ft.Row([
                            self.cliente_field,
                        ], spacing=20),
                    ], spacing=15),
                    padding=ft.Padding(25, 20, 25, 20),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                    border_radius=12,
                    bgcolor=DarkTheme.CARD_BG,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Resumen financiero
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CALCULATE, color=DarkTheme.SUCCESS, size=24),
                            ft.Text("Resumen Financiero", size=20, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ], spacing=10),
                        ft.Divider(color=DarkTheme.DIVIDER_COLOR, height=20),
                        self.total_venta_text,
                        self.ganancia_estimada_text,
                    ], spacing=15),
                    padding=ft.Padding(25, 20, 25, 20),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                    border_radius=12,
                    bgcolor=DarkTheme.CARD_BG,
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Botones de acción
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CANCEL, size=20),
                                ft.Text("Cancelar", weight=ft.FontWeight.W_600)
                            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                            on_click=self._cerrar_formulario,
                            style=ft.ButtonStyle(
                                bgcolor=DarkTheme.BUTTON_SECONDARY,
                                color=DarkTheme.PRIMARY_TEXT,
                                elevation={"": 4, "hovered": 8},
                                shadow_color=ft.Colors.BLACK26,
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.Padding(25, 15, 25, 15)
                            ),
                            width=200,
                            height=50
                        ),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.SAVE, size=20),
                                ft.Text("Registrar Venta", weight=ft.FontWeight.W_600)
                            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                            on_click=self._on_save,
                            style=ft.ButtonStyle(
                                bgcolor=DarkTheme.BUTTON_SUCCESS,
                                color=DarkTheme.PRIMARY_TEXT,
                                elevation={"": 4, "hovered": 8},
                                shadow_color=ft.Colors.BLACK26,
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.Padding(25, 15, 25, 15)
                            ),
                            width=200,
                            height=50
                        ),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(0, 20, 0, 20)
                ),
            ], spacing=0, scroll=ft.ScrollMode.AUTO),
            padding=ft.Padding(40, 30, 40, 30),
            bgcolor=DarkTheme.SECONDARY_BG,
            expand=True
        )
        
        # Contenedor principal para toda la ventana
        self.form_container = ft.Container(
            content=ft.Column([
                header,
                form_content,
            ], spacing=0, expand=True),
            bgcolor=DarkTheme.PRIMARY_BG,
            expand=True
        )
    
    def _on_producto_changed(self, e):
        """Maneja el cambio de producto seleccionado"""
        if not e.data:
            return
        
        # Buscar el producto seleccionado
        producto_seleccionado = None
        for producto in self.productos_disponibles:
            if producto['id_producto'] == e.data:
                producto_seleccionado = producto
                break
        
        if producto_seleccionado:
            # Actualizar información del producto
            info_text = f"""
Producto: {producto_seleccionado['nombre']}
Stock disponible: {producto_seleccionado['stock_actual']} ml
Costo de entrada: Q{producto_seleccionado['costo_entrada']:.2f}
Proveedor: {producto_seleccionado['proveedor']}
            """.strip()
            
            self.info_producto.content = ft.Text(
                info_text,
                color=DarkTheme.PRIMARY_TEXT,
                size=14
            )
            
            # Verificar y alertar si el stock es bajo
            if producto_seleccionado['stock_actual'] < 50:
                self.alert_manager.show_warning(
                    f"⚠️ Stock bajo detectado\n\n"
                    f"Producto: {producto_seleccionado['nombre']}\n"
                    f"Stock actual: {producto_seleccionado['stock_actual']:.1f} ml\n\n"
                    f"Considere reabastecer después de esta venta"
                )
            
            # Sugerir precio basado en margen del 100%
            costo_por_ml = producto_seleccionado['costo_por_ml']
            precio_sugerido = costo_por_ml * 2  # Margen del 100%
            self.precio_unitario_field.value = f"{precio_sugerido:.2f}"
            
            self._calcular_total(None)
            self.page.update()
    
    def _calcular_total(self, e):
        """Calcula el total de la venta y ganancia estimada"""
        try:
            cantidad = float(self.cantidad_field.value or 0)
            precio_unitario = float(self.precio_unitario_field.value or 0)
            
            total_venta = cantidad * precio_unitario
            self.total_venta_text.value = f"Total: Q{total_venta:.2f}"
            
            # Calcular ganancia estimada si hay producto seleccionado
            if self.producto_dropdown.value:
                producto_seleccionado = None
                for producto in self.productos_disponibles:
                    if producto['id_producto'] == self.producto_dropdown.value:
                        producto_seleccionado = producto
                        break
                
                if producto_seleccionado:
                    costo_por_ml = producto_seleccionado['costo_por_ml']
                    costo_total = cantidad * costo_por_ml
                    ganancia_estimada = total_venta - costo_total
                    
                    # Mostrar ganancia con indicador visual
                    if ganancia_estimada >= 0:
                        self.ganancia_estimada_text.value = f"Ganancia estimada: Q{ganancia_estimada:.2f} ✅"
                        self.ganancia_estimada_text.color = DarkTheme.SUCCESS
                    else:
                        self.ganancia_estimada_text.value = f"Pérdida estimada: Q{abs(ganancia_estimada):.2f} ⚠️"
                        self.ganancia_estimada_text.color = DarkTheme.ERROR
            else:
                self.ganancia_estimada_text.value = "Ganancia estimada: Q0.00"
                self.ganancia_estimada_text.color = DarkTheme.SECONDARY_TEXT
            
            self.page.update()
            
        except ValueError:
            # Si hay error en la conversión, mostrar 0
            self.total_venta_text.value = "Total: Q0.00"
            self.ganancia_estimada_text.value = "Ganancia estimada: Q0.00"
            self.ganancia_estimada_text.color = DarkTheme.SECONDARY_TEXT
            self.page.update()
            # Si hay error en la conversión, mostrar 0
            self.total_venta_text.value = "Total: Q0.00"
            self.ganancia_estimada_text.value = "Ganancia estimada: Q0.00"
            self.page.update()
    
    def _on_save(self, e):
        """Maneja el evento de guardar"""
        if not self._validar_formulario():
            return
        
        try:
            cantidad = float(self.cantidad_field.value)
            precio_unitario = float(self.precio_unitario_field.value)
            precio_total = cantidad * precio_unitario
            
            # Obtener información del producto para la confirmación
            producto_seleccionado = None
            for producto in self.productos_disponibles:
                if producto['id_producto'] == self.producto_dropdown.value:
                    producto_seleccionado = producto
                    break
            
            # Calcular ganancia estimada
            ganancia_estimada = 0
            if producto_seleccionado:
                costo_total = cantidad * producto_seleccionado['costo_por_ml']
                ganancia_estimada = precio_total - costo_total
            
            # Mostrar confirmación con detalles de la venta
            producto_nombre = producto_seleccionado['nombre'] if producto_seleccionado else "Desconocido"
            cliente_nombre = self.cliente_field.value.strip() or "Cliente general"
            
            # Alerta de confirmación detallada
            self.alert_manager.show_info(
                f"Confirmar venta:\n\n"
                f"📦 Producto: {producto_nombre}\n"
                f"🧪 Cantidad: {cantidad:.1f} ml\n"
                f"👤 Cliente: {cliente_nombre}\n"
                f"💰 Total: Q{precio_total:.2f}\n"
                f"📈 Ganancia: Q{ganancia_estimada:.2f}\n\n"
                f"¿Desea continuar con el registro?"
            )
            
            data = {
                'producto_id': self.producto_dropdown.value,
                'cantidad': cantidad,
                'precio_venta': precio_total,
                'cliente': self.cliente_field.value.strip() or None
            }
            
            if self.on_save:
                result = self.on_save(data)
                if result:
                    self._cerrar_formulario()
            
        except Exception as ex:
            if self.alert_manager:
                self.alert_manager.show_error(f"Error inesperado al procesar la venta: {str(ex)}")
    
    def _on_cancel(self, e):
        """Maneja el evento de cancelar"""
        if self.on_cancel:
            self.on_cancel()
        self._cerrar_formulario()
    
    def _validar_formulario(self):
        """Valida los datos del formulario"""
        if not self.producto_dropdown.value:
            if self.alert_manager:
                self.alert_manager.show_warning("⚠️ Selección requerida\nDebe seleccionar un producto para continuar")
            return False
        
        try:
            cantidad = float(self.cantidad_field.value)
            precio_unitario = float(self.precio_unitario_field.value)
            
            if cantidad <= 0:
                if self.alert_manager:
                    self.alert_manager.show_warning("⚠️ Cantidad inválida\nLa cantidad debe ser mayor a 0 ml")
                return False
            
            if precio_unitario <= 0:
                if self.alert_manager:
                    self.alert_manager.show_warning("⚠️ Precio inválido\nEl precio unitario debe ser mayor a Q0.00")
                return False
            
            # Verificar stock disponible
            producto_seleccionado = None
            for producto in self.productos_disponibles:
                if producto['id_producto'] == self.producto_dropdown.value:
                    producto_seleccionado = producto
                    break
            
            if producto_seleccionado and cantidad > producto_seleccionado['stock_actual']:
                if self.alert_manager:
                    self.alert_manager.show_error(
                        f"❌ Stock insuficiente\n\n"
                        f"Producto: {producto_seleccionado['nombre']}\n"
                        f"Stock disponible: {producto_seleccionado['stock_actual']:.1f} ml\n"
                        f"Cantidad solicitada: {cantidad:.1f} ml\n\n"
                        f"Reduzca la cantidad o reabastezca el producto"
                    )
                return False
            
            # Validar si el precio es muy bajo (menos del costo)
            if producto_seleccionado:
                costo_total = cantidad * producto_seleccionado['costo_por_ml']
                precio_total = cantidad * precio_unitario
                
                if precio_total < costo_total:
                    if self.alert_manager:
                        self.alert_manager.show_warning(
                            f"⚠️ Precio por debajo del costo\n\n"
                            f"Costo del producto: Q{costo_total:.2f}\n"
                            f"Precio de venta: Q{precio_total:.2f}\n"
                            f"Pérdida: Q{(costo_total - precio_total):.2f}\n\n"
                            f"¿Está seguro del precio?"
                        )
            
            return True
            
        except ValueError:
            if self.alert_manager:
                self.alert_manager.show_error("❌ Datos inválidos\nVerifique que la cantidad y el precio sean números válidos")
            return False
    
    def _cerrar_formulario(self, e=None):
        """Cierra el formulario y vuelve a la ventana principal"""
        if self.original_content:
            self.page.clean()
            for control in self.original_content:
                self.page.add(control)
            self.page.update()
    
    def show(self):
        """Muestra el formulario como ventana completa"""
        # Guardar el contenido original
        self.original_content = self.page.controls.copy()
        
        # Limpiar la página y mostrar el formulario
        self.page.clean()
        self.page.add(self.form_container)
        self.page.update()
    
    def mostrar(self):
        """Alias para show - compatibilidad"""
        self.show()
    
    def set_callbacks(self, on_save=None, on_cancel=None):
        """Establece los callbacks del formulario"""
        if on_save:
            self.on_save = on_save
        if on_cancel:
            self.on_cancel = on_cancel