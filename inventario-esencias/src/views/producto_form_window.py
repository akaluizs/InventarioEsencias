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
        
        # Detectar tipo de producto basándose en la estructura de datos
        tipo_inicial = "esencia"  # Por defecto
        if producto_data:
            # Si tiene capacidad_ml, es un frasco
            if 'capacidad_ml' in producto_data:
                tipo_inicial = "frasco"
        
        # Controles del formulario
        self.tipo_producto_field = ft.Dropdown(
            label="Tipo de Producto",
            width=300,
            options=[
                ft.dropdown.Option("esencia", "🧪 Esencia"),
                ft.dropdown.Option("frasco", "📦 Frasco"),
            ],
            value=tipo_inicial,
            on_change=self._on_tipo_changed,
            text_style=ft.TextStyle(color=DarkTheme.PRIMARY_TEXT),
            label_style=ft.TextStyle(color=DarkTheme.SECONDARY_TEXT),
            bgcolor=DarkTheme.SURFACE_BG,
            border_color=DarkTheme.BORDER_COLOR,
            focused_border_color=DarkTheme.INFO
        )
        
        # Campo ID con prefijo automático
        # Extraer parte personalizada del ID si está editando
        id_personalizado = ""
        if producto_data and 'id_producto' in producto_data:
            id_completo = str(producto_data['id_producto'])
            # Remover prefijos conocidos para mostrar solo la parte personalizada
            if id_completo.startswith("ESE"):
                id_personalizado = id_completo[3:]
            elif id_completo.startswith("F"):
                id_personalizado = id_completo[1:]
            else:
                id_personalizado = id_completo
        
        # Contenedor para mostrar el prefijo + campo editable
        self.prefijo_text = ft.Text(
            "ESE",  # Prefijo por defecto para esencias
            size=16,
            weight=ft.FontWeight.BOLD,
            color=DarkTheme.INFO
        )
        
        self.id_personalizado_field = ft.TextField(
            label="ID Personalizado", 
            width=200,
            disabled=self.is_editing,
            value=id_personalizado,
            hint_text="Ej: 001, Lavanda, etc.",
            on_change=self._actualizar_id_completo
        )
        
        # Campo oculto que contendrá el ID completo (prefijo + personalizado)
        self.id_field = ft.TextField(
            label="ID Completo", 
            width=300,
            disabled=True,  # Siempre deshabilitado, se genera automáticamente
            value=str(producto_data['id_producto']) if producto_data else "ESE"
        )
        
        # Texto de preview del ID (se creará después en la interfaz)
        self._preview_id_text = None
        
        # Crear el contenedor de ejemplo de cálculo
        self.ejemplo_calculo_container = ft.Container(
            content=ft.Column([
                ft.Text("💡 Ejemplo de cálculo:", size=12, weight=ft.FontWeight.BOLD, color=DarkTheme.INFO),
                ft.Text("Si tienes 8 ml y costó Q80 → Costo por ml = Q80 ÷ 8 ml = Q10 por ml", 
                       size=11, color=DarkTheme.SECONDARY_TEXT, italic=True),
            ], spacing=2),
            padding=ft.Padding(10, 5, 10, 5),
            bgcolor=DarkTheme.SURFACE_BG,
            border_radius=5,
            visible=True
        )
        self.nombre_field = ft.TextField(
            label="Nombre de la Esencia", 
            width=400,
            value=producto_data['nombre'] if producto_data else ""
        )
        self.genero_field = ft.Dropdown(
            label="Género",
            width=300,
            options=[
                ft.dropdown.Option("Masculino", "Masculino"),
                ft.dropdown.Option("Femenino", "Femenino"),
                ft.dropdown.Option("Unisex", "Unisex"),
            ],
            value=producto_data.get('genero', 'Unisex') if producto_data else 'Unisex',
            text_style=ft.TextStyle(color=DarkTheme.PRIMARY_TEXT),
            label_style=ft.TextStyle(color=DarkTheme.SECONDARY_TEXT),
            bgcolor=DarkTheme.SURFACE_BG,
            border_color=DarkTheme.BORDER_COLOR,
            focused_border_color=DarkTheme.INFO
        )
        
        # Campos para ESENCIAS
        self.stock_actual_field = ft.TextField(
            label="Stock Actual (ml)", 
            width=250, 
            value=str(producto_data['stock_actual']) if producto_data else "0",
            on_change=self._calcular_costo_por_ml
        )
        self.costo_entrada_field = ft.TextField(
            label="Costo de Entrada (Q)", 
            width=250, 
            value=str(producto_data['costo_entrada']) if producto_data else "0.00",
            on_change=self._calcular_costo_por_ml
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
            label="Costo por ml (Q) - Calculado automáticamente", 
            width=350, 
            value=str(producto_data['costo_por_ml']) if producto_data else "0.00",
            disabled=True,  # Solo lectura, se calcula automáticamente
            bgcolor=DarkTheme.SURFACE_BG,
            color=DarkTheme.INFO  # Color diferente para indicar que es calculado
        )
        
        # Campos para FRASCOS
        self.capacidad_ml_field = ft.TextField(
            label="Capacidad (ml)",
            width=250,
            value=str(producto_data.get('capacidad_ml', '')) if producto_data else "0",
            visible=False
        )
        self.stock_frascos_field = ft.TextField(
            label="Stock Actual (cantidad)",
            width=250,
            value=str(producto_data.get('stock_actual', '')) if producto_data else "0",
            visible=False
        )
        self.costo_frasco_field = ft.TextField(
            label="Costo por Frasco (Q)",
            width=250,
            value=str(producto_data.get('costo_frasco', producto_data.get('costo', ''))) if producto_data else "0.00",
            visible=False
        )
        
        self._create_form_content()
        # Note: _on_tipo_changed se ejecutará después de crear la interfaz
    
    def _on_tipo_changed(self, e):
        """Cambia la visibilidad de los campos según el tipo de producto"""
        tipo = self.tipo_producto_field.value
        is_esencia = tipo == "esencia"
        
        # Actualizar prefijo según el tipo
        if is_esencia:
            self.prefijo_text.value = "ESE"
        else:
            self.prefijo_text.value = "F"
        
        # Actualizar ID completo con el nuevo prefijo
        self._actualizar_id_completo(None)
        
        # Campos exclusivos de esencias
        self.genero_field.visible = is_esencia
        self.proveedor_field.visible = is_esencia
        self.fecha_caducidad_field.visible = is_esencia
        self.costo_por_ml_field.visible = is_esencia
        self.ejemplo_calculo_container.visible = is_esencia
        
        # Campos exclusivos de frascos
        self.capacidad_ml_field.visible = not is_esencia
        self.stock_frascos_field.visible = not is_esencia
        self.costo_frasco_field.visible = not is_esencia
        
        # Actualizar labels según el tipo
        if is_esencia:
            self.nombre_field.label = "Nombre de la Esencia"
            self.stock_actual_field.label = "Stock Actual (ml)"
            self.costo_entrada_field.label = "Costo de Entrada (Q)"
        else:
            self.nombre_field.label = "Nombre del Frasco"
            self.stock_actual_field.visible = False  # No usar este campo para frascos
            self.costo_entrada_field.visible = False  # No usar este campo para frascos
        
        # Actualizar la página
        if hasattr(self, 'page') and self.page:
            self.page.update()
        
        # Calcular costo por ml si es una esencia
        if is_esencia:
            self._calcular_costo_por_ml(None)
    
    def _actualizar_id_completo(self, e):
        """Actualiza el ID completo combinando prefijo + ID personalizado"""
        prefijo = self.prefijo_text.value
        id_personalizado = self.id_personalizado_field.value.strip()
        
        if id_personalizado:
            id_completo = f"{prefijo}{id_personalizado}"
        else:
            id_completo = prefijo
        
        self.id_field.value = id_completo
        
        # Actualizar el texto de preview del ID completo solo si existe
        if hasattr(self, '_preview_id_text') and self._preview_id_text is not None:
            self._preview_id_text.value = f"ID Completo: {id_completo}"
        
        # Actualizar la página si es necesario
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def _calcular_costo_por_ml(self, e):
        """Calcula automáticamente el costo por ml basado en costo de entrada y stock actual"""
        try:
            costo_entrada = float(self.costo_entrada_field.value or 0)
            stock_actual = float(self.stock_actual_field.value or 0)
            
            if stock_actual > 0:
                costo_por_ml = costo_entrada / stock_actual
                self.costo_por_ml_field.value = f"{costo_por_ml:.4f}"
            else:
                self.costo_por_ml_field.value = "0.0000"
            
            # Actualizar la página
            if hasattr(self, 'page') and self.page:
                self.page.update()
                
        except ValueError:
            # Si hay error en la conversión, mantener el valor actual
            self.costo_por_ml_field.value = "0.0000"
            if hasattr(self, 'page') and self.page:
                self.page.update()
    
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
                            self.tipo_producto_field,
                        ], wrap=True, spacing=15),
                        # Sección de ID con prefijo + personalizado
                        ft.Column([
                            ft.Text("Identificador del Producto", size=14, weight=ft.FontWeight.BOLD, color=DarkTheme.SECONDARY_TEXT),
                            ft.Row([
                                ft.Container(
                                    content=self.prefijo_text,
                                    padding=ft.Padding(15, 15, 5, 15),
                                    bgcolor=DarkTheme.INFO,
                                    border_radius=ft.border_radius.only(top_left=8, bottom_left=8),
                                    alignment=ft.alignment.center
                                ),
                                self.id_personalizado_field,
                            ], spacing=0),
                            ft.Container(
                                content=ft.Text(f"ID Completo: {self.id_field.value}", 
                                               size=12, 
                                               color=DarkTheme.SECONDARY_TEXT,
                                               italic=True),
                                padding=ft.Padding(5, 5, 5, 0)
                            ),
                        ], spacing=5),
                        ft.Row([
                            self.nombre_field,
                        ], wrap=True, spacing=15),
                        ft.Row([
                            self.genero_field,  # Solo para esencias
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
                        # Campos para esencias
                        ft.Row([
                            self.stock_actual_field,  # Solo para esencias (ml)
                        ], wrap=True, spacing=15),
                        # Campos para frascos
                        ft.Row([
                            self.capacidad_ml_field,   # Solo para frascos
                            self.stock_frascos_field,  # Solo para frascos
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
                        # Campos para esencias
                        ft.Row([
                            self.costo_entrada_field,  # Solo para esencias
                            self.costo_por_ml_field,   # Solo para esencias
                        ], wrap=True, spacing=15),
                        # Ejemplo del cálculo (solo para esencias)
                        self.ejemplo_calculo_container,
                        # Campos para frascos
                        ft.Row([
                            self.costo_frasco_field,   # Solo para frascos
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
                        # Solo para esencias
                        ft.Row([
                            self.proveedor_field,       # Solo para esencias
                            self.fecha_caducidad_field, # Solo para esencias
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
            tipo = self.tipo_producto_field.value
            
            if tipo == "esencia":
                # Datos para esencia
                data = {
                    'tipo_producto': 'esencia',
                    'id_producto': self.id_field.value,
                    'nombre': self.nombre_field.value,
                    'genero': self.genero_field.value,
                    'stock_actual': float(self.stock_actual_field.value),
                    'costo_entrada': float(self.costo_entrada_field.value),
                    'proveedor': self.proveedor_field.value,
                    'fecha_caducidad': self.fecha_caducidad_field.value,
                    'costo_por_ml': float(self.costo_por_ml_field.value)
                }
            else:  # frasco
                # Datos para frasco
                data = {
                    'tipo_producto': 'frasco',
                    'id_producto': self.id_field.value,
                    'nombre': self.nombre_field.value,
                    'capacidad_ml': float(self.capacidad_ml_field.value),
                    'stock_actual': float(self.stock_frascos_field.value),
                    'costo': float(self.costo_frasco_field.value)
                }
            
            if self.on_save:
                self.on_save(data, self.is_editing)
            
            self.close()
            
        except Exception as ex:
            self._mostrar_error(f"Error al guardar: {str(ex)}")
    
    def _validar_formulario(self):
        """Valida los datos del formulario"""
        if not self.id_field.value.strip():
            self._mostrar_error("El ID del producto es requerido")
            return False
        
        if not self.nombre_field.value.strip():
            self._mostrar_error("El nombre del producto es requerido")
            return False
        
        tipo = self.tipo_producto_field.value
        
        if tipo == "esencia":
            # Validaciones específicas para esencias
            if not self.proveedor_field.value.strip():
                self._mostrar_error("El proveedor es requerido para esencias")
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
        
        else:  # frasco
            # Validaciones específicas para frascos
            try:
                capacidad = float(self.capacidad_ml_field.value)
                stock_frascos = float(self.stock_frascos_field.value)
                costo_frasco = float(self.costo_frasco_field.value)
                
                if capacidad <= 0:
                    self._mostrar_error("La capacidad debe ser mayor que 0")
                    return False
                
                if stock_frascos < 0:
                    self._mostrar_error("El stock de frascos no puede ser negativo")
                    return False
                
                if costo_frasco < 0:
                    self._mostrar_error("El costo del frasco no puede ser negativo")
                    return False
                    
            except ValueError:
                self._mostrar_error("Los valores numéricos deben ser válidos")
                return False
        
        return True
    
    def _on_cancel(self, e):
        """Maneja el evento de cancelar"""
        if self.on_cancel:
            self.on_cancel()
        self.close()
    
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
        
        # Configurar visibilidad inicial de campos después de mostrar la interfaz
        self._on_tipo_changed(None)
    
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
