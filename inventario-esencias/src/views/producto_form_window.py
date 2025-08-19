import flet as ft
from typing import Optional, Callable, Dict, Any
from utils.alerts import AlertManager

class DarkTheme:
    """Colores para el tema oscuro moderno"""
    # Fondos
    PRIMARY_BG = ft.Colors.GREY_900
    SECONDARY_BG = ft.Colors.GREY_800
    CARD_BG = ft.Colors.GREY_700
    SURFACE_BG = ft.Colors.GREY_600
    HOVER_BG = ft.Colors.GREY_600
    
    # Textos
    PRIMARY_TEXT = ft.Colors.WHITE
    SECONDARY_TEXT = ft.Colors.GREY_300
    ACCENT_TEXT = ft.Colors.BLUE_300
    
    # Acentos modernos
    SUCCESS = ft.Colors.GREEN_400
    ERROR = ft.Colors.RED_400
    WARNING = ft.Colors.ORANGE_400
    INFO = ft.Colors.BLUE_400
    
    # Botones modernos
    BUTTON_PRIMARY = ft.Colors.BLUE_600
    BUTTON_SUCCESS = ft.Colors.GREEN_600
    BUTTON_DANGER = ft.Colors.RED_600
    BUTTON_SECONDARY = ft.Colors.GREY_600
    
    # Bordes y divisores
    BORDER_COLOR = ft.Colors.GREY_600
    DIVIDER_COLOR = ft.Colors.GREY_500

class ProductoFormWindow:
    def __init__(self, page: ft.Page, producto_data: Optional[Dict[str, Any]] = None):
        self.page = page
        self.producto_data = producto_data
        self.is_editing = producto_data is not None
        
        # Sistema de alertas
        self.alert_manager = AlertManager(page)
        
        # Callbacks
        self.on_save: Optional[Callable] = None
        self.on_cancel: Optional[Callable] = None
        
        # Guardar el contenido original de la página
        self.original_content = None
        
        # Controles del formulario
        self.id_field = ft.TextField(
            label="ID Producto", 
            width=300,
            disabled=self.is_editing,
            value=str(producto_data['id_producto']) if producto_data else ""
        )
        self.nombre_field = ft.TextField(
            label="Nombre de la Esencia", 
            width=400,
            value=producto_data['nombre'] if producto_data else ""
        )
        self.stock_actual_field = ft.TextField(
            label="Stock Actual (ml)", 
            width=250, 
            value=str(producto_data['stock_actual']) if producto_data else "0"
        )
        self.costo_entrada_field = ft.TextField(
            label="Costo de Entrada (Q)", 
            width=250, 
            value=str(producto_data['costo_entrada']) if producto_data else "0.00"
        )
        self.proveedor_field = ft.TextField(
            label="Proveedor", 
            width=350,
            value=producto_data['proveedor'] if producto_data else ""
        )
        self.fecha_caducidad_field = ft.TextField(
            label="Fecha de Caducidad (YYYY-MM-DD)", 
            width=300,
            hint_text="2024-12-31",
            value=producto_data['fecha_caducidad'] if producto_data else ""
        )
        self.costo_por_ml_field = ft.TextField(
            label="Costo por ml (Q)", 
            width=250, 
            value=str(producto_data['costo_por_ml']) if producto_data else "0.00"
        )
        
        self._create_form_content()
    
    def _create_form_content(self):
        """Crea el contenido del formulario como página completa"""
        title_text = "Editar Producto" if self.is_editing else "Agregar Nuevo Producto"
        title_icon = ft.Icons.EDIT if self.is_editing else ft.Icons.ADD
        
        # Encabezado
        header = ft.Container(
            content=ft.Row([
                ft.Icon(title_icon, color=DarkTheme.INFO, size=30),
                ft.Text(title_text, size=28, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT),
                ft.Container(expand=True),  # Spacer
                ft.IconButton(
                    ft.Icons.CLOSE,
                    tooltip="Cerrar",
                    on_click=self._on_cancel,
                    icon_size=30,
                    icon_color=DarkTheme.ERROR
                )
            ]),
            padding=20,
            bgcolor=DarkTheme.CARD_BG,
            border_radius=ft.border_radius.only(top_left=10, top_right=10)
        )
        
        # Formulario principal
        form_content = ft.Container(
            content=ft.Column([
                # Información básica
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.INFO, color=DarkTheme.INFO),
                            ft.Text("Información Básica", size=18, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ]),
                        ft.Divider(color=DarkTheme.SECONDARY_TEXT),
                        ft.Row([
                            self.id_field,
                            self.nombre_field,
                        ], wrap=True, spacing=15),
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(2, DarkTheme.SECONDARY_TEXT),
                    border_radius=10,
                    bgcolor=DarkTheme.CARD_BG
                ),
                
                # Control de Stock
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.INVENTORY, color=DarkTheme.SUCCESS),
                            ft.Text("Control de Stock", size=18, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ]),
                        ft.Divider(color=DarkTheme.SECONDARY_TEXT),
                        ft.Row([
                            self.stock_actual_field,
                        ], wrap=True, spacing=15),
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(2, DarkTheme.SECONDARY_TEXT),
                    border_radius=10,
                    bgcolor=DarkTheme.CARD_BG
                ),
                
                # Información Financiera
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.ATTACH_MONEY, color=DarkTheme.WARNING),
                            ft.Text("Información Financiera", size=18, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ]),
                        ft.Divider(color=DarkTheme.SECONDARY_TEXT),
                        ft.Row([
                            self.costo_entrada_field,
                            self.costo_por_ml_field,
                        ], wrap=True, spacing=15),
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(2, DarkTheme.SECONDARY_TEXT),
                    border_radius=10,
                    bgcolor=DarkTheme.CARD_BG
                ),
                
                # Información adicional
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.BUSINESS, color=DarkTheme.WARNING),
                            ft.Text("Información Adicional", size=18, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ]),
                        ft.Divider(color=DarkTheme.SECONDARY_TEXT),
                        ft.Row([
                            self.proveedor_field,
                            self.fecha_caducidad_field,
                        ], wrap=True, spacing=15),
                    ], spacing=10),
                    padding=20,
                    border=ft.border.all(2, DarkTheme.SECONDARY_TEXT),
                    border_radius=10,
                    bgcolor=DarkTheme.CARD_BG
                ),
            ], spacing=20, scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True
        )
        
        # Botones de acción
        action_buttons = ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Cancelar",
                    icon=ft.Icons.CANCEL,
                    on_click=self._on_cancel,
                    style=ft.ButtonStyle(
                        bgcolor=DarkTheme.SECONDARY_BG,
                        color=DarkTheme.PRIMARY_TEXT
                    ),
                    width=150,
                    height=50
                ),
                ft.Container(expand=True),  # Spacer
                ft.ElevatedButton(
                    "Guardar" if not self.is_editing else "Actualizar",
                    icon=ft.Icons.SAVE if not self.is_editing else ft.Icons.UPDATE,
                    on_click=self._on_save,
                    style=ft.ButtonStyle(
                        bgcolor=DarkTheme.SUCCESS if not self.is_editing else DarkTheme.INFO,
                        color=DarkTheme.PRIMARY_TEXT
                    ),
                    width=150,
                    height=50
                ),
            ]),
            padding=20,
            bgcolor=DarkTheme.CARD_BG,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
        )
        
        # Contenedor principal
        self.form_container = ft.Container(
            content=ft.Column([
                header,
                form_content,
                action_buttons,
            ], spacing=0),
            border=ft.border.all(2, DarkTheme.SECONDARY_BG),
            border_radius=10,
            bgcolor=DarkTheme.CARD_BG,
            margin=20
        )
    
    def _on_save(self, e):
        """Maneja el evento de guardar"""
        if not self._validar_formulario():
            return
        
        try:
            data = {
                'id_producto': self.id_field.value,
                'nombre': self.nombre_field.value,
                'stock_actual': float(self.stock_actual_field.value),
                'costo_entrada': float(self.costo_entrada_field.value),
                'proveedor': self.proveedor_field.value,
                'fecha_caducidad': self.fecha_caducidad_field.value,
                'costo_por_ml': float(self.costo_por_ml_field.value)
            }
            
            if self.on_save:
                self.on_save(data, self.is_editing)
            
            self.close()
            
        except Exception as ex:
            self._mostrar_error(f"Error al guardar: {str(ex)}")
    
    def _on_cancel(self, e):
        """Maneja el evento de cancelar"""
        if self.on_cancel:
            self.on_cancel()
        self.close()
    
    def _validar_formulario(self):
        """Valida los datos del formulario"""
        if not self.id_field.value.strip():
            self._mostrar_error("El ID del producto es requerido")
            return False
        
        if not self.nombre_field.value.strip():
            self._mostrar_error("El nombre del producto es requerido")
            return False
        
        if not self.proveedor_field.value.strip():
            self._mostrar_error("El proveedor es requerido")
            return False
        
        try:
            stock_actual = float(self.stock_actual_field.value)
            costo_entrada = float(self.costo_entrada_field.value)
            costo_ml = float(self.costo_por_ml_field.value)
            
            if stock_actual < 0:
                self._mostrar_error("El stock actual no puede ser negativo")
                return False
            
            if costo_entrada < 0:
                self._mostrar_error("El costo de entrada no puede ser negativo")
                return False
            
            if costo_ml < 0:
                self._mostrar_error("El costo por ml no puede ser negativo")
                return False
                
        except ValueError:
            self._mostrar_error("Los valores de stock y costo deben ser números válidos")
            return False
        
        # Validar formato de fecha básico
        if self.fecha_caducidad_field.value:
            try:
                parts = self.fecha_caducidad_field.value.split('-')
                if len(parts) != 3:
                    raise ValueError("Formato incorrecto")
                year, month, day = map(int, parts)
                if not (1 <= month <= 12 and 1 <= day <= 31 and year >= 2024):
                    raise ValueError("Fecha inválida")
            except ValueError:
                self._mostrar_error("Formato de fecha inválido. Use YYYY-MM-DD")
                return False
        
        return True
    
    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.alert_manager.show_error(mensaje)
    
    def show(self):
        """Muestra el formulario reemplazando el contenido de la página"""
        # Guardar el contenido actual
        self.original_content = self.page.controls.copy()
        
        # Limpiar la página y agregar el formulario
        self.page.clean()
        self.page.add(self.form_container)
        self.page.update()
    
    def close(self):
        """Cierra el formulario y restaura el contenido original"""
        if self.original_content:
            self.page.clean()
            for control in self.original_content:
                self.page.add(control)
            self.page.update()
    
    def set_callbacks(self, on_save: Callable, on_cancel: Optional[Callable] = None):
        """Establece los callbacks"""
        self.on_save = on_save
        self.on_cancel = on_cancel
