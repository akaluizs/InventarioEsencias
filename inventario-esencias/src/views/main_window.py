import flet as ft
from datetime import datetime
from typing import List, Optional, Callable
from views.producto_form_window import ProductoFormWindow
from utils.alerts import AlertManager

class DarkTheme:
    """Colores para el tema oscuro"""
    # Fondos
    PRIMARY_BG = ft.Colors.GREY_900
    SECONDARY_BG = ft.Colors.GREY_800
    CARD_BG = ft.Colors.GREY_700
    SURFACE_BG = ft.Colors.GREY_600
    HOVER_BG = ft.Colors.GREY_600
    TABLE_ROW_EVEN = "#424242"  # Gris más claro para filas pares
    TABLE_ROW_ODD = "#383838"   # Gris más oscuro para filas impares
    
    # Textos
    PRIMARY_TEXT = ft.Colors.WHITE
    SECONDARY_TEXT = ft.Colors.GREY_300
    ACCENT_TEXT = ft.Colors.BLUE_300
    MUTED_TEXT = ft.Colors.GREY_400
    
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
    
    # Colores especiales
    ACCENT = ft.Colors.CYAN_400
    HIGHLIGHT = ft.Colors.PURPLE_400

class MainWindow:
    def __init__(self, page: ft.Page):
        self.page = page
        self.productos = []
        self.productos_filtrados = []
        
        # Sistema de alertas
        self.alert_manager = AlertManager(page)
        
        # Callbacks para el controlador
        self.on_agregar_producto: Optional[Callable] = None
        self.on_actualizar_producto: Optional[Callable] = None
        self.on_eliminar_producto: Optional[Callable] = None
        self.on_cargar_productos: Optional[Callable] = None
        self.on_mostrar_salidas: Optional[Callable] = None
        self.on_mostrar_historial: Optional[Callable] = None
        
        # Botones de acción principales con diseño moderno
        self.btn_nuevo_producto = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=20),
                ft.Text("Nuevo Producto", weight=ft.FontWeight.W_600)
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            on_click=self._abrir_formulario_nuevo,
            style=ft.ButtonStyle(
                bgcolor=DarkTheme.BUTTON_SUCCESS,
                color=DarkTheme.PRIMARY_TEXT,
                elevation={"": 4, "hovered": 8},
                shadow_color=ft.Colors.BLACK26,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 12, 20, 12)
            ),
            width=200,
            height=56
        )
        
        self.btn_salida = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.SELL_OUTLINED, size=20),
                ft.Text("Ventas", weight=ft.FontWeight.W_600)
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            on_click=self._abrir_formulario_salidas,
            style=ft.ButtonStyle(
                bgcolor=DarkTheme.BUTTON_SUCCESS,
                color=DarkTheme.PRIMARY_TEXT,
                elevation={"": 4, "hovered": 8},
                shadow_color=ft.Colors.BLACK26,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 12, 20, 12)
            ),
            width=200,
            height=56
        )
        
        self.btn_historial = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.HISTORY, size=20),
                ft.Text("Historial", weight=ft.FontWeight.W_600)
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            on_click=self._abrir_historial_ventas,
            style=ft.ButtonStyle(
                bgcolor=DarkTheme.BUTTON_PRIMARY,
                color=DarkTheme.PRIMARY_TEXT,
                elevation={"": 4, "hovered": 8},
                shadow_color=ft.Colors.BLACK26,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 12, 20, 12)
            ),
            width=200,
            height=56
        )
        
        self.btn_actualizar_lista = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.REFRESH_ROUNDED, size=20),
                ft.Text("Actualizar", weight=ft.FontWeight.W_600)
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            on_click=self._actualizar_lista,
            style=ft.ButtonStyle(
                bgcolor=DarkTheme.BUTTON_SECONDARY,
                color=DarkTheme.PRIMARY_TEXT,
                elevation={"": 2, "hovered": 6},
                shadow_color=ft.Colors.BLACK26,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 12, 20, 12)
            ),
            width=200,
            height=56
        )
        
        # Campo de búsqueda mejorado
        self.search_field = ft.Container(
            content=ft.TextField(
                label="Buscar productos...",
                on_change=self._filtrar_productos,
                prefix_icon=ft.Icons.SEARCH_ROUNDED,
                width=400,
                height=56,
                color=DarkTheme.PRIMARY_TEXT,
                bgcolor=DarkTheme.CARD_BG,
                border_color=DarkTheme.BORDER_COLOR,
                border_radius=ft.border_radius.all(12),
                content_padding=ft.Padding(16, 12, 16, 12),
                text_style=ft.TextStyle(size=16)
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 2)
            ),
            border_radius=ft.border_radius.all(12)
        )
        
        # Filtros mejorados
        self.filtro_stock_bajo = ft.Container(
            content=ft.Checkbox(
                label="Solo productos con stock bajo",
                on_change=self._filtrar_productos,
                label_style=ft.TextStyle(
                    color=DarkTheme.PRIMARY_TEXT,
                    size=14,
                    weight=ft.FontWeight.W_500
                ),
                check_color=DarkTheme.SUCCESS,
                active_color=DarkTheme.SUCCESS
            ),
            padding=ft.Padding(16, 8, 16, 8),
            bgcolor=DarkTheme.CARD_BG,
            border_radius=ft.border_radius.all(8)
        )
        
        # Filtro por género
        self.filtro_genero = ft.Container(
            content=ft.Dropdown(
                label="Filtrar por género",
                options=[
                    ft.dropdown.Option("Todos", "Todos"),
                    ft.dropdown.Option("Masculino", "Masculino"),
                    ft.dropdown.Option("Femenino", "Femenino"),
                    ft.dropdown.Option("Unisex", "Unisex"),
                ],
                value="Todos",
                on_change=self._filtrar_productos,
                text_style=ft.TextStyle(color=DarkTheme.PRIMARY_TEXT),
                label_style=ft.TextStyle(color=DarkTheme.SECONDARY_TEXT),
                bgcolor=DarkTheme.SURFACE_BG,
                border_color=DarkTheme.BORDER_COLOR,
                focused_border_color=DarkTheme.ACCENT,
                width=200
            ),
            padding=ft.Padding(16, 8, 16, 8),
            bgcolor=DarkTheme.CARD_BG,
            border_radius=ft.border_radius.all(8)
        )
        
        # Filtro por tipo de producto
        self.filtro_tipo = ft.Container(
            content=ft.Dropdown(
                label="Filtrar por tipo",
                options=[
                    ft.dropdown.Option("esencia", "🌸 Esencias"),
                    ft.dropdown.Option("frasco", "🍶 Frascos"),
                ],
                value="esencia",  # Por defecto mostrar esencias
                on_change=self._filtrar_productos,
                text_style=ft.TextStyle(color=DarkTheme.PRIMARY_TEXT),
                label_style=ft.TextStyle(color=DarkTheme.SECONDARY_TEXT),
                bgcolor=DarkTheme.SURFACE_BG,
                border_color=DarkTheme.BORDER_COLOR,
                focused_border_color=DarkTheme.ACCENT,
                width=200
            ),
            padding=ft.Padding(16, 8, 16, 8),
            bgcolor=DarkTheme.CARD_BG,
            border_radius=ft.border_radius.all(8)
        )
        
        # Contenedor para la tabla de productos moderna
        self.productos_container = self._crear_tabla_productos()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        self.page.title = "Inventario de Esencias"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        
        # Encabezado principal 
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.SCIENCE_ROUNDED, size=44, color=DarkTheme.SUCCESS),
                    bgcolor=DarkTheme.SUCCESS + "20",
                    padding=8,
                    border_radius=12
                ),
                ft.Text(
                    "Inventario de Esencias 🧪",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=DarkTheme.PRIMARY_TEXT
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.Padding(30, 25, 30, 25),
            bgcolor=DarkTheme.SECONDARY_BG,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 2)
            )
        )
        
        # Barra de herramientas 
        toolbar = ft.Container(
            content=ft.Column([
                # Primera fila: Botones principales
                ft.Row([
                    self.btn_nuevo_producto,
                    self.btn_actualizar_lista,
                    self.btn_salida,
                    self.btn_historial
                ], spacing=20, alignment=ft.MainAxisAlignment.START),
                
                # Segunda fila: Búsqueda y filtros
                ft.Row([
                    self.search_field,
                    self.filtro_stock_bajo,
                    self.filtro_genero,
                    self.filtro_tipo,
                ], spacing=20, alignment=ft.MainAxisAlignment.START, wrap=True),
            ], spacing=20),
            padding=ft.Padding(30, 20, 30, 20),
            border=ft.border.all(1, DarkTheme.SECONDARY_TEXT),
            border_radius=10,
            bgcolor=DarkTheme.CARD_BG,
            margin=ft.margin.only(left=20, right=20, top=30, bottom=10)  # Más espacio arriba
        )

        # Sección de estadísticas
        self.stats_container = ft.Container(
            content=self._crear_estadisticas(),
            padding=ft.Padding(25, 12, 25, 18),
            margin=ft.margin.only(top=35, bottom=20)  # Más espacio arriba y abajo
        )
        
        # Sección de tabla 
        seccion_tabla = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.TABLE_CHART_ROUNDED, size=24, color=DarkTheme.ACCENT_TEXT),
                        ft.Text("Lista de Productos", size=22, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT),
                    ], spacing=12, alignment=ft.MainAxisAlignment.START),
                    padding=ft.Padding(0, 0, 0, 15)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=self.productos_container,
                            expand=True,
                        )
                    ], scroll=ft.ScrollMode.ALWAYS, expand=True),
                    border_radius=ft.border_radius.all(12),
                    padding=ft.Padding(16, 12, 16, 12),
                    bgcolor=DarkTheme.CARD_BG,
                    expand=True,  # Hace que la tabla ocupe todo el espacio disponible
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.BLACK26,
                        offset=ft.Offset(0, 2)
                    ),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR)
                )
            ], spacing=0, expand=True),
            padding=ft.Padding(20, 0, 20, 20),
            expand=True  # Permite que la sección ocupe todo el espacio disponible
        )
        
        # Layout principal optimizado para ocupar todo el espacio
        main_content = ft.Column([
            header,
            toolbar,
            self.stats_container,
            seccion_tabla,
        ], spacing=0, expand=True)
        
        # Container principal que ocupa toda la página
        self.page.add(main_content)
        
        # Cargar productos iniciales
        if self.on_cargar_productos:
            self.on_cargar_productos()
    
    def _crear_estadisticas(self):
        """Crea tarjetas de estadísticas modernas con efectos hover"""
        # Separar esencias y frascos por estructura de datos
        esencias = [p for p in self.productos if 'capacidad_ml' not in p]
        frascos = [p for p in self.productos if 'capacidad_ml' in p]
        
        total_productos = len(self.productos)
        total_esencias = len(esencias)
        total_frascos = len(frascos)
        productos_bajo_stock = len([p for p in self.productos if self._necesita_reabastecimiento(p)])
        valor_total_inventario = sum(self._calcular_valor_total(p) for p in self.productos)
        
        def crear_tarjeta_stat(icono, titulo, valor, color_icono, color_valor, descripcion=""):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icono, size=28, color=color_icono),
                            bgcolor=color_icono + "20",  # Color con transparencia
                            border_radius=50,
                            padding=10,
                            width=48,
                            height=48
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(titulo, size=13, weight=ft.FontWeight.W_500, color=DarkTheme.SECONDARY_TEXT),
                                ft.Text(str(valor), size=28, weight=ft.FontWeight.BOLD, color=color_valor),
                                ft.Text(descripcion, size=10, color=DarkTheme.MUTED_TEXT) if descripcion else ft.Container()
                            ], spacing=3, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
                            expand=True
                        )
                    ], alignment=ft.MainAxisAlignment.START, spacing=12),
                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.Padding(18, 16, 18, 16),
                bgcolor=DarkTheme.CARD_BG,
                border_radius=ft.border_radius.all(14),
                expand=True,  # Permite que las tarjetas se expandan uniformemente
                height=100,   # Altura aumentada para que el texto no se corte
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.BLACK38,
                    offset=ft.Offset(0, 3)
                ),
                border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                on_hover=lambda e: self._on_stat_card_hover(e, e.control)
            )
        
        return ft.Row([
            crear_tarjeta_stat(
                ft.Icons.INVENTORY_2_ROUNDED, 
                "Total Productos", 
                total_productos, 
                DarkTheme.INFO,
                DarkTheme.PRIMARY_TEXT,
                f"{total_esencias} esencias, {total_frascos} frascos"
            ),
            crear_tarjeta_stat(
                ft.Icons.WARNING_ROUNDED, 
                "Stock Bajo", 
                productos_bajo_stock, 
                DarkTheme.WARNING if productos_bajo_stock > 0 else DarkTheme.SUCCESS,
                DarkTheme.WARNING if productos_bajo_stock > 0 else DarkTheme.SUCCESS,
                "requieren reposición"
            ),
            crear_tarjeta_stat(
                ft.Icons.ATTACH_MONEY_ROUNDED, 
                "Valor Total", 
                f"Q{valor_total_inventario:.2f}", 
                DarkTheme.SUCCESS,
                DarkTheme.SUCCESS,
                "valor del inventario"
            ),
            crear_tarjeta_stat(
                ft.Icons.LIQUOR,
                "Esencias",
                total_esencias,
                DarkTheme.ACCENT,
                DarkTheme.ACCENT,
                "productos aromáticos"
            ),
            crear_tarjeta_stat(
                ft.Icons.INVENTORY,
                "Frascos",
                total_frascos,
                DarkTheme.INFO,
                DarkTheme.INFO,
                "contenedores disponibles"
            ),
        ], spacing=16, alignment=ft.MainAxisAlignment.SPACE_EVENLY)  
    
    def _crear_tabla_productos(self):
        """Crea la tabla moderna de productos similar al historial"""
        # Crear encabezados dinámicos
        self.headers_container = ft.Container(
            content=self._crear_encabezados_tabla(),
            bgcolor=DarkTheme.SECONDARY_BG,
            padding=15,
            border_radius=ft.border_radius.only(top_left=10, top_right=10)
        )
        
        self.productos_filas = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)
        
        return ft.Container(
            content=ft.Column([
                self.headers_container,
                ft.Container(
                    content=self.productos_filas,
                    padding=ft.Padding(25, 15, 25, 25),
                    bgcolor=DarkTheme.CARD_BG,
                    border_radius=ft.border_radius.only(bottom_left=12, bottom_right=12),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                    height=400,  # Altura fija para asegurar visibilidad
                    expand=True
                )
            ], spacing=0),
            expand=True
        )
        
    def _crear_encabezados_tabla(self):
        """Crea los encabezados de la tabla según el tipo de producto seleccionado"""
        tipo_seleccionado = self.filtro_tipo.content.value if hasattr(self, 'filtro_tipo') else "esencia"
        
        if tipo_seleccionado == "frasco":
            # Encabezados específicos para frascos
            return ft.Row([
                ft.Container(ft.Text("ID", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=80, alignment=ft.alignment.center),
                ft.Container(ft.Text("Nombre", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=180, alignment=ft.alignment.center),
                ft.Container(ft.Text("Capacidad", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=90, alignment=ft.alignment.center),
                ft.Container(ft.Text("Stock (unidades)", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text("Costo", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                ft.Container(ft.Text("Valor Total", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text("Estado", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                ft.Container(ft.Text("Acciones", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=140, alignment=ft.alignment.center),
            ], spacing=15)
        else:  # esencia
            # Encabezados específicos para esencias
            return ft.Row([
                ft.Container(ft.Text("ID", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=80, alignment=ft.alignment.center),
                ft.Container(ft.Text("Nombre", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=180, alignment=ft.alignment.center),
                ft.Container(ft.Text("Género", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=90, alignment=ft.alignment.center),
                ft.Container(ft.Text("Stock (ml)", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text("Costo Entrada", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                ft.Container(ft.Text("Proveedor", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=140, alignment=ft.alignment.center),
                ft.Container(ft.Text("Caducidad", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text("Costo/ml", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                ft.Container(ft.Text("Valor Total", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text("Estado", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                ft.Container(ft.Text("Acciones", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=140, alignment=ft.alignment.center),
            ], spacing=15)
    
    def _on_product_row_hover(self, e):
        """Maneja el hover en las filas de productos"""
        if e.data == "true":
            e.control.scale = 1.02
            e.control.elevation = 6
        else:
            e.control.scale = 1.0
            e.control.elevation = 2
        e.control.update()
    
    def _on_stat_card_hover(self, e, card):
        """Efecto hover para las tarjetas de estadísticas"""
        try:
            if e.data == "true":  # Mouse enter
                card.bgcolor = DarkTheme.HOVER_BG
                card.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=16,
                    color=ft.Colors.BLACK45,
                    offset=ft.Offset(0, 6)
                )
            else:  # Mouse leave
                card.bgcolor = DarkTheme.CARD_BG
                card.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color=ft.Colors.BLACK38,
                    offset=ft.Offset(0, 4)
                )
            # Usar page.update() en lugar de card.update() para evitar errores
            if hasattr(self, 'page') and self.page:
                self.page.update()
        except Exception as ex:
            # Ignorar errores de hover para no interrumpir la aplicación
            print(f"Error en hover effect: {ex}")
    
    def _abrir_formulario_nuevo(self, e):
        """Abre el formulario para agregar un nuevo producto"""
        print("Abriendo formulario para nuevo producto...")  # Debug
        try:
            form_window = ProductoFormWindow(self.page)
            form_window.set_callbacks(
                on_save=self._on_producto_saved,
                on_cancel=None
            )
            form_window.show()
            print("Formulario mostrado correctamente")  # Debug
        except Exception as ex:
            print(f"Error al abrir formulario: {ex}")  # Debug
            self._mostrar_mensaje(f"Error al abrir formulario: {str(ex)}", ft.Colors.RED)
    
    def _abrir_formulario_editar(self, producto):
        """Abre el formulario para editar un producto"""
        form_window = ProductoFormWindow(self.page, producto)
        form_window.set_callbacks(
            on_save=self._on_producto_saved,
            on_cancel=None
        )
        form_window.show()
    
    def _abrir_formulario_salidas(self, e):
        """Abre el formulario de salidas/ventas"""
        if self.on_mostrar_salidas:
            self.on_mostrar_salidas()
        else:
            self.alert_manager.show_toast("Funcionalidad de ventas no disponible", "error")
    
    def _abrir_historial_ventas(self, e):
        """Abre la ventana del historial de ventas"""
        if self.on_mostrar_historial:
            self.on_mostrar_historial()
        else:
            self.alert_manager.show_toast("Funcionalidad de historial no disponible", "error")
    
    def _actualizar_lista(self, e):
        """Actualiza la lista de productos"""
        if self.on_cargar_productos:
            self.on_cargar_productos()
            self.alert_manager.show_toast("Lista actualizada", "info")
    
    def _on_producto_saved(self, data, is_editing):
        """Maneja cuando se guarda un producto desde el formulario"""
        try:
            tipo = data.get('tipo_producto', 'esencia')
            
            if tipo == 'esencia':
                # Manejar esencias
                if is_editing:
                    if self.on_actualizar_producto:
                        self.on_actualizar_producto(
                            data['id_producto'],
                            data['nombre'],
                            data['genero'],
                            data['stock_actual'],
                            data['costo_entrada'],
                            data['proveedor'],
                            data['fecha_caducidad'],
                            data['costo_por_ml']
                        )
                        self.alert_manager.show_success(
                            f"✅ Esencia '{data['nombre']}' actualizada correctamente"
                        )
                else:
                    if self.on_agregar_producto:
                        self.on_agregar_producto(
                            data['id_producto'],
                            data['nombre'],
                            data['genero'],
                            data['stock_actual'],
                            data['costo_entrada'],
                            data['proveedor'],
                            data['fecha_caducidad'],
                            data['costo_por_ml']
                        )
                        self.alert_manager.show_success(
                            f"🌸 Esencia '{data['nombre']}' agregada correctamente"
                        )
            
            else:  # frasco
                # Manejar frascos
                if is_editing:
                    if self.on_actualizar_frasco:
                        self.on_actualizar_frasco(
                            data['id_producto'],
                            data['nombre'],
                            data['capacidad_ml'],
                            data['stock_actual'],
                            data['costo']
                        )
                        self.alert_manager.show_success(
                            f"✅ Frasco '{data['nombre']}' actualizado correctamente"
                        )
                else:
                    if self.on_agregar_frasco:
                        self.on_agregar_frasco(
                            data['id_producto'],
                            data['nombre'],
                            data['capacidad_ml'],
                            data['stock_actual'],
                            data['costo']
                        )
                        self.alert_manager.show_success(
                            f"🍶 Frasco '{data['nombre']}' agregado correctamente"
                        )
            
        except Exception as ex:
            action = "actualizar" if is_editing else "agregar"
            tipo_texto = "esencia" if data.get('tipo_producto') == 'esencia' else "frasco"
            self.alert_manager.show_error(
                f"❌ Error al {action} {tipo_texto}: {str(ex)}"
            )
    
    def _mostrar_mensaje(self, mensaje, color):
        """Muestra un mensaje al usuario"""
        from utils.alerts import AlertManager
        
        # Determinar el tipo de alerta basado en el color
        if color == ft.Colors.RED:
            AlertManager.show_alert(self.page, mensaje, "error")
        elif color == ft.Colors.GREEN:
            AlertManager.show_alert(self.page, mensaje, "success")
        elif color == ft.Colors.ORANGE:
            AlertManager.show_alert(self.page, mensaje, "warning")
        else:
            AlertManager.show_alert(self.page, mensaje, "info")
    
    def _eliminar_producto(self, producto_id):
        """Elimina un producto y sus ventas asociadas automáticamente"""
        print(f"DEBUG: Ejecutando eliminación para producto ID: {producto_id}")
        print(f"DEBUG: Callback eliminar disponible: {self.on_eliminar_producto is not None}")
        
        if self.on_eliminar_producto:
            try:
                print(f"DEBUG: Llamando callback de eliminación")
                resultado = self.on_eliminar_producto(producto_id)
                
                if resultado:
                    self.alert_manager.show_success(
                        f"🗑️ Producto '{producto_id}' eliminado del inventario\n\n"
                        f"✅ El historial de ventas se mantiene para auditoría"
                    )
                    print(f"DEBUG: Eliminación exitosa")
                else:
                    self.alert_manager.show_error(
                        f"❌ No se pudo eliminar el producto '{producto_id}'"
                    )
                    print(f"DEBUG: Eliminación falló - callback retornó False")
                    
            except Exception as ex:
                print(f"DEBUG: Error en eliminación: {ex}")
                self.alert_manager.show_error(
                    f"❌ Error: {str(ex)}"
                )
        else:
            print(f"DEBUG: No hay callback de eliminación configurado")
    
    def _filtrar_productos(self, e=None):
        """Filtra los productos según los criterios"""
        texto_busqueda = self.search_field.content.value.lower() if self.search_field.content.value else ""
        solo_stock_bajo = self.filtro_stock_bajo.content.value
        genero_seleccionado = self.filtro_genero.content.value
        tipo_seleccionado = self.filtro_tipo.content.value
        
        self.productos_filtrados = []
        
        for producto in self.productos:
            # Filtro por texto - funciona para ambos tipos
            coincide_texto = (
                texto_busqueda in producto['nombre'].lower() or
                texto_busqueda in str(producto.get('proveedor', '')).lower() or
                texto_busqueda in str(producto['id_producto'])
            )
            
            # Filtro por stock bajo - diferente para frascos y esencias
            stock_bajo = self._necesita_reabastecimiento(producto)
            coincide_stock = not solo_stock_bajo or stock_bajo
            
            # Filtro por tipo de producto
            es_frasco = 'capacidad_ml' in producto
            if tipo_seleccionado == "frasco":
                coincide_tipo = es_frasco
            elif tipo_seleccionado == "esencia":
                coincide_tipo = not es_frasco
            else:
                coincide_tipo = True  # Por si acaso hay algún valor inesperado
            
            # Filtro por género - solo aplica a esencias
            es_frasco = 'capacidad_ml' in producto
            if es_frasco:
                # Los frascos siempre pasan el filtro de género
                coincide_genero = True
            else:
                # Solo filtrar por género en esencias
                coincide_genero = (genero_seleccionado == "Todos" or 
                                 producto.get('genero', 'Unisex') == genero_seleccionado)
            
            if coincide_texto and coincide_stock and coincide_genero and coincide_tipo:
                self.productos_filtrados.append(producto)
        
        self._actualizar_tabla()
    
    def _necesita_reabastecimiento(self, producto):
        """Verifica si un producto necesita reabastecimiento"""
        es_frasco = 'capacidad_ml' in producto
        if es_frasco:
            # Para frascos: stock bajo si tienen menos de 5 unidades
            return producto['stock_actual'] < 5
        else:
            # Para esencias: stock bajo si tienen menos de 50ml
            return producto['stock_actual'] < 50
    
    def _calcular_valor_total(self, producto):
        """Calcula el valor total del stock de un producto"""
        es_frasco = 'capacidad_ml' in producto
        if es_frasco:
            # Para frascos: stock * costo por frasco
            return producto['stock_actual'] * producto.get('costo_frasco', producto.get('costo', 0))
        else:
            # Para esencias: stock * costo por ml
            return producto['stock_actual'] * producto['costo_por_ml']
    
    def _actualizar_tabla(self):
        """Actualiza la tabla moderna de productos"""
        # Actualizar encabezados según el filtro seleccionado
        if hasattr(self, 'headers_container'):
            self.headers_container.content = self._crear_encabezados_tabla()
        
        # Limpiar filas actuales
        self.productos_filas.controls.clear()
        
        productos_a_mostrar = self.productos_filtrados if hasattr(self, 'productos_filtrados') else self.productos
        tipo_seleccionado = self.filtro_tipo.content.value if hasattr(self, 'filtro_tipo') else "esencia"
        
        for i, producto in enumerate(productos_a_mostrar):
            necesita_restock = self._necesita_reabastecimiento(producto)
            valor_total = self._calcular_valor_total(producto)
            
            # Estado del producto
            estado_color = DarkTheme.ERROR if necesita_restock else DarkTheme.SUCCESS
            estado_texto = "⚠️ Stock Bajo" if necesita_restock else "✅ OK"
            
            # Color alternado para filas
            row_color = DarkTheme.TABLE_ROW_EVEN if i % 2 == 0 else DarkTheme.TABLE_ROW_ODD
            
            # Detectar tipo de producto por su estructura
            es_frasco = 'capacidad_ml' in producto
            
            # Generar fila según el tipo de producto
            if es_frasco:
                fila = self._crear_fila_frasco(producto, estado_color, estado_texto, valor_total, row_color)
            else:
                fila = self._crear_fila_esencia(producto, estado_color, estado_texto, valor_total, row_color)
            
            if fila:
                self.productos_filas.controls.append(fila)
        
        # Actualizar la página si existe
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def _crear_fila_frasco(self, producto, estado_color, estado_texto, valor_total, row_color):
        """Crea una fila específica para frascos"""
        return ft.Container(
            content=ft.Row([
                ft.Container(ft.Text(str(producto['id_producto']), color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=80, alignment=ft.alignment.center),
                ft.Container(ft.Text(producto['nombre'], color=DarkTheme.PRIMARY_TEXT, size=13, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER), width=180, alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LIQUOR, size=16, color=DarkTheme.INFO),
                        ft.Text(f"{producto.get('capacidad_ml', 0)} ml", color=DarkTheme.PRIMARY_TEXT, size=12, text_align=ft.TextAlign.CENTER)
                    ], tight=True, spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                    width=90, alignment=ft.alignment.center
                ),
                ft.Container(ft.Text(f"{producto['stock_actual']} unidades", color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text(f"Q{producto.get('costo_frasco', producto.get('costo_entrada', 0)):.2f}", color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                ft.Container(ft.Text(f"Q{valor_total:.2f}", color=DarkTheme.SUCCESS, size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text(estado_texto, color=estado_color, size=13, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                self._crear_botones_accion(producto)
            ], spacing=15),
            bgcolor=row_color,
            padding=15,
            border_radius=8
        )
    
    def _crear_fila_esencia(self, producto, estado_color, estado_texto, valor_total, row_color):
        """Crea una fila específica para esencias"""
        return ft.Container(
            content=ft.Row([
                ft.Container(ft.Text(str(producto['id_producto']), color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=80, alignment=ft.alignment.center),
                ft.Container(ft.Text(producto['nombre'], color=DarkTheme.PRIMARY_TEXT, size=13, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER), width=180, alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(
                            self._get_icono_genero(producto.get('genero', 'Unisex')),
                            size=16,
                            color=self._get_color_genero(producto.get('genero', 'Unisex'))
                        ),
                        ft.Text(producto.get('genero', 'Unisex'), color=DarkTheme.PRIMARY_TEXT, size=12, text_align=ft.TextAlign.CENTER)
                    ], tight=True, spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                    width=90, alignment=ft.alignment.center
                ),
                ft.Container(ft.Text(f"{producto['stock_actual']} ml", color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text(f"Q{producto['costo_entrada']:.2f}", color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                ft.Container(ft.Text(producto['proveedor'], color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=140, alignment=ft.alignment.center),
                ft.Container(ft.Text(producto['fecha_caducidad'], color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text(f"Q{producto['costo_por_ml']:.2f}", color=DarkTheme.ACCENT, size=13, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                ft.Container(ft.Text(f"Q{valor_total:.2f}", color=DarkTheme.SUCCESS, size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text(estado_texto, color=estado_color, size=13, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                self._crear_botones_accion(producto)
            ], spacing=15),
            bgcolor=row_color,
            padding=15,
            border_radius=8
        )
    
    def _crear_fila_mixta(self, producto, estado_color, estado_texto, valor_total, row_color):
        """Crea una fila para vista mixta (esencias y frascos)"""
        # Preparar columnas específicas según el tipo de producto
        if producto.get('tipo_producto') == 'frasco':
            columna_tipo = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.LIQUOR, size=16, color=DarkTheme.INFO),
                    ft.Text(f"{producto.get('capacidad_ml', 0)} ml", color=DarkTheme.PRIMARY_TEXT, size=12, text_align=ft.TextAlign.CENTER)
                ], tight=True, spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                width=90, alignment=ft.alignment.center
            )
            columna_stock = ft.Container(ft.Text(f"{producto['stock_actual']} unidades", color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center)
            columna_info = ft.Container(ft.Text("Frasco", color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=140, alignment=ft.alignment.center)
            columna_fecha = ft.Container(ft.Text("N/A", color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center)
            columna_costo_unidad = ft.Container(ft.Text(f"Q{producto['costo_por_ml']:.4f}/ml", color=DarkTheme.ACCENT, size=13, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center)
        else:
            columna_tipo = ft.Container(
                content=ft.Row([
                    ft.Icon(
                        self._get_icono_genero(producto.get('genero', 'Unisex')),
                        size=16,
                        color=self._get_color_genero(producto.get('genero', 'Unisex'))
                    ),
                    ft.Text(producto.get('genero', 'Unisex'), color=DarkTheme.PRIMARY_TEXT, size=12, text_align=ft.TextAlign.CENTER)
                ], tight=True, spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                width=90, alignment=ft.alignment.center
            )
            columna_stock = ft.Container(ft.Text(f"{producto['stock_actual']} ml", color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center)
            columna_info = ft.Container(ft.Text(producto['proveedor'], color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=140, alignment=ft.alignment.center)
            columna_fecha = ft.Container(ft.Text(producto['fecha_caducidad'], color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center)
            columna_costo_unidad = ft.Container(ft.Text(f"Q{producto['costo_por_ml']:.2f}", color=DarkTheme.ACCENT, size=13, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center)
        
        return ft.Container(
            content=ft.Row([
                ft.Container(ft.Text(str(producto['id_producto']), color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=80, alignment=ft.alignment.center),
                ft.Container(ft.Text(producto['nombre'], color=DarkTheme.PRIMARY_TEXT, size=13, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER), width=180, alignment=ft.alignment.center),
                columna_tipo,
                columna_stock,
                ft.Container(ft.Text(f"Q{producto['costo_entrada']:.2f}", color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                columna_info,
                columna_fecha,
                columna_costo_unidad,
                ft.Container(ft.Text(f"Q{valor_total:.2f}", color=DarkTheme.SUCCESS, size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                ft.Container(ft.Text(estado_texto, color=estado_color, size=13, text_align=ft.TextAlign.CENTER), width=100, alignment=ft.alignment.center),
                self._crear_botones_accion(producto)
            ], spacing=15),
            bgcolor=row_color,
            padding=15,
            border_radius=8
        )
    
    def _crear_botones_accion(self, producto):
        """Crea los botones de acción para cada fila"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.IconButton(
                        ft.Icons.EDIT_ROUNDED,
                        tooltip="Editar producto",
                        icon_color=DarkTheme.INFO,
                        icon_size=18,
                        on_click=lambda e, p=producto: self._abrir_formulario_editar(p)
                    ),
                    bgcolor=DarkTheme.INFO + "20",
                    border_radius=6,
                    padding=2
                ),
                ft.Container(
                    content=ft.IconButton(
                        ft.Icons.DELETE_ROUNDED,
                        tooltip="Eliminar producto",
                        icon_color=DarkTheme.ERROR,
                        icon_size=18,
                        on_click=lambda e, pid=producto['id_producto']: self._confirmar_eliminacion(pid)
                    ),
                    bgcolor=DarkTheme.ERROR + "20",
                    border_radius=6,
                    padding=2
                )
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            width=140,
            alignment=ft.alignment.center
        )
    
    def _confirmar_eliminacion(self, producto_id):
        """Muestra diálogo de confirmación para eliminar"""
        print(f"DEBUG: Iniciando confirmación de eliminación para producto ID: {producto_id}")
        
        # Buscar el nombre del producto para mostrar en la confirmación
        producto_nombre = None
        for producto in self.productos:
            if producto['id_producto'] == producto_id:
                producto_nombre = producto['nombre']
                break
        
        print(f"DEBUG: Producto encontrado: {producto_nombre}")
        mensaje = f"¿Estás seguro de que quieres eliminar el producto '{producto_nombre or producto_id}'?"
        
        print(f"DEBUG: Mostrando diálogo de confirmación")
        self.alert_manager.show_confirmation_dialog(
            titulo="Confirmar Eliminación",
            mensaje=mensaje,
            on_confirm=lambda: self._eliminar_producto(producto_id),
            on_cancel=lambda: self.alert_manager.show_info("Eliminación cancelada")
        )
    
    # Métodos públicos para ser llamados por el controlador
    def mostrar_productos(self, productos: List[dict]):
        """Muestra la lista de productos en la tabla"""
        self.productos = productos
        self.productos_filtrados = productos.copy()
        
        # Actualizar estadísticas con los nuevos productos
        self.stats_container.content = self._crear_estadisticas()
        
        # Aplicar filtros después de cargar los productos
        self._filtrar_productos()
    
    def actualizar_tabla(self, productos: List[dict]):
        """Actualiza la tabla con nueva lista de productos"""
        self.mostrar_productos(productos)
    
    def set_callbacks(self, agregar_callback, actualizar_callback, eliminar_callback, cargar_callback, salidas_callback, historial_callback, agregar_frasco_callback=None, actualizar_frasco_callback=None):
        """Establece los callbacks para las operaciones"""
        self.on_agregar_producto = agregar_callback
        self.on_actualizar_producto = actualizar_callback
        self.on_eliminar_producto = eliminar_callback
        self.on_cargar_productos = cargar_callback
        self.on_mostrar_salidas = salidas_callback
        self.on_mostrar_historial = historial_callback
        self.on_agregar_frasco = agregar_frasco_callback
        self.on_actualizar_frasco = actualizar_frasco_callback
    
    def _get_icono_genero(self, genero):
        """Obtiene el ícono correspondiente al género"""
        iconos = {
            'Masculino': ft.Icons.MALE,
            'Femenino': ft.Icons.FEMALE,
            'Unisex': ft.Icons.PEOPLE
        }
        return iconos.get(genero, ft.Icons.PEOPLE)
    
    def _get_color_genero(self, genero):
        """Obtiene el color correspondiente al género"""
        colores = {
            'Masculino': ft.Colors.BLUE_400,
            'Femenino': ft.Colors.PINK_400,
            'Unisex': ft.Colors.PURPLE_400
        }
        return colores.get(genero, ft.Colors.PURPLE_400)
