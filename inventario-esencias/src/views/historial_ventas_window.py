import flet as ft
from datetime import datetime
from typing import List, Dict
from utils.alerts import AlertManager

class DarkTheme:
    """Colores para el tema oscuro"""
    # Fondos
    PRIMARY_BG = ft.Colors.GREY_900
    SECONDARY_BG = ft.Colors.GREY_800
    CARD_BG = ft.Colors.GREY_700
    SURFACE_BG = ft.Colors.GREY_600
    HOVER_BG = ft.Colors.GREY_600
    TABLE_ROW_EVEN = "#424242"
    TABLE_ROW_ODD = "#383838"
    
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

class HistorialVentasWindow:
    def __init__(self, page: ft.Page, salida_service, producto_service):
        self.page = page
        self.salida_service = salida_service
        self.producto_service = producto_service
        
        # Sistema de alertas
        self.alert_manager = AlertManager(page)
        
        # Guardar el contenido original de la página
        self.original_content = None
        
        # Datos
        self.historial_ventas = []
        self.estadisticas = {}
        
        # Crear la interfaz
        self._crear_interfaz()
        self._cargar_datos()
    
    def _crear_interfaz(self):
        """Crea la interfaz de usuario"""
        # Encabezado
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=DarkTheme.PRIMARY_TEXT,
                    on_click=self._volver,
                    tooltip="Volver"
                ),
                ft.Icon(ft.Icons.HISTORY, size=40, color=DarkTheme.INFO),
                ft.Text(
                    "Historial de Ventas",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=DarkTheme.PRIMARY_TEXT
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.START),
            padding=ft.Padding(30, 20, 30, 20),
            bgcolor=DarkTheme.PRIMARY_BG,
        )
        
        # Tarjetas de estadísticas
        self.stats_container = ft.Container(
            content=self._crear_estadisticas(),
            padding=ft.Padding(30, 25, 30, 25),
            margin=ft.margin.only(left=0, right=0, bottom=20),
            alignment=ft.alignment.center,
            bgcolor=DarkTheme.SECONDARY_BG,
        )
        
        # Filtros y búsqueda
        self.filtros_container = ft.Container(
            content=ft.Row([
                ft.TextField(
                    label="Buscar producto",
                    width=300,
                    border_color=DarkTheme.BORDER_COLOR,
                    focused_border_color=DarkTheme.ACCENT,
                    text_style=ft.TextStyle(color=DarkTheme.PRIMARY_TEXT),
                    label_style=ft.TextStyle(color=DarkTheme.SECONDARY_TEXT),
                    on_change=self._filtrar_historial
                ),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.REFRESH, size=20),
                        ft.Text("Actualizar")
                    ], spacing=8),
                    on_click=self._actualizar_datos,
                    style=ft.ButtonStyle(
                        bgcolor=DarkTheme.BUTTON_PRIMARY,
                        color=DarkTheme.PRIMARY_TEXT,
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.START),
            padding=ft.Padding(30, 20, 30, 10),
            bgcolor=DarkTheme.CARD_BG,
            border_radius=10,
            margin=ft.margin.only(left=30, right=30, bottom=20)
        )
        
        # Tabla de historial
        self.tabla_container = ft.Container(
            content=self._crear_tabla_historial(),
            padding=ft.Padding(30, 20, 30, 30),
            bgcolor=DarkTheme.SECONDARY_BG,
            expand=True
        )
        
        # Container principal
        self.main_container = ft.Container(
            content=ft.Column([
                header,
                self.stats_container,
                self.filtros_container,
                self.tabla_container,
            ], spacing=0, expand=True),
            bgcolor=DarkTheme.PRIMARY_BG,
            expand=True
        )
    
    def _crear_estadisticas(self):
        """Crea las tarjetas de estadísticas"""
        def crear_stat_card(titulo, valor, icono, color):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icono, size=28, color=color),
                            padding=ft.Padding(12, 12, 12, 12),
                            bgcolor=f"{color}20",  # Color con transparencia
                            border_radius=50,
                            width=52,
                            height=52
                        ),
                        ft.Column([
                            ft.Text(titulo, size=14, color=DarkTheme.SECONDARY_TEXT, weight=ft.FontWeight.W_500),
                            ft.Text(str(valor), size=24, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
                    ], spacing=20, alignment=ft.MainAxisAlignment.START)
                ], spacing=15),
                padding=ft.Padding(25, 22, 25, 22),
                bgcolor=DarkTheme.CARD_BG,
                border_radius=15,
                border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                width=280,
                height=110,
                animate_scale=200,
                on_hover=lambda e, card=None: self._on_stat_card_hover(e, card)
            )
        
        return ft.Row([
            crear_stat_card("Total Ventas", 0, ft.Icons.SHOPPING_CART, DarkTheme.INFO),
            crear_stat_card("Ingresos", "Q0.00", ft.Icons.ATTACH_MONEY, DarkTheme.SUCCESS),
            crear_stat_card("Ganancia", "Q0.00", ft.Icons.TRENDING_UP, DarkTheme.WARNING),
            crear_stat_card("Promedio", "Q0.00", ft.Icons.ANALYTICS, DarkTheme.ACCENT),
        ], spacing=25, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
    
    def _on_stat_card_hover(self, e, card):
        """Maneja el hover en las tarjetas de estadísticas"""
        if e.data == "true":
            e.control.scale = 1.05
            e.control.elevation = 8
        else:
            e.control.scale = 1.0
            e.control.elevation = 4
        e.control.update()
    
    def _crear_tabla_historial(self):
        """Crea la tabla del historial"""
        # Encabezados de la tabla con mejor distribución
        headers = ft.Row([
            ft.Container(ft.Text("Fecha", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=160, alignment=ft.alignment.center),
            ft.Container(ft.Text("ID Venta", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
            ft.Container(ft.Text("Producto", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=250, alignment=ft.alignment.center),
            ft.Container(ft.Text("Cantidad", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
            ft.Container(ft.Text("Precio", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
            ft.Container(ft.Text("Ganancia", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
            ft.Container(ft.Text("Cliente", weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT, size=14, text_align=ft.TextAlign.CENTER), width=200, alignment=ft.alignment.center),
        ], spacing=15)
        
        self.tabla_filas = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=headers,
                    padding=ft.Padding(25, 18, 25, 18),
                    bgcolor=DarkTheme.SURFACE_BG,
                    border_radius=ft.border_radius.only(top_left=12, top_right=12),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR)
                ),
                ft.Container(
                    content=self.tabla_filas,
                    padding=ft.Padding(25, 15, 25, 25),
                    bgcolor=DarkTheme.CARD_BG,
                    border_radius=ft.border_radius.only(bottom_left=12, bottom_right=12),
                    border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                    expand=True
                )
            ], spacing=0),
            expand=True,
            margin=ft.margin.only(left=30, right=30, bottom=30)
        )
    
    def _cargar_datos(self):
        """Carga los datos del historial y estadísticas"""
        try:
            # Cargar historial
            self.historial_ventas = self.salida_service.obtener_historial_ventas()
            
            # Cargar estadísticas
            self.estadisticas = self.salida_service.obtener_estadisticas_ventas()
            
            # Actualizar la interfaz
            self._actualizar_estadisticas()
            self._actualizar_tabla()
            
        except Exception as e:
            self.alert_manager.show_error(f"Error al cargar datos: {str(e)}")
    
    def _actualizar_estadisticas(self):
        """Actualiza las tarjetas de estadísticas"""
        stats = self.estadisticas
        
        def crear_stat_card(titulo, valor, icono, color):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icono, size=28, color=color),
                            padding=ft.Padding(12, 12, 12, 12),
                            bgcolor=f"{color}20",  # Color con transparencia
                            border_radius=50,
                            width=52,
                            height=52
                        ),
                        ft.Column([
                            ft.Text(titulo, size=14, color=DarkTheme.SECONDARY_TEXT, weight=ft.FontWeight.W_500),
                            ft.Text(str(valor), size=24, weight=ft.FontWeight.BOLD, color=DarkTheme.PRIMARY_TEXT)
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
                    ], spacing=20, alignment=ft.MainAxisAlignment.START)
                ], spacing=15),
                padding=ft.Padding(25, 22, 25, 22),
                bgcolor=DarkTheme.CARD_BG,
                border_radius=15,
                border=ft.border.all(1, DarkTheme.BORDER_COLOR),
                width=280,
                height=110,
                animate_scale=200,
                on_hover=lambda e, card=None: self._on_stat_card_hover(e, card)
            )
        
        self.stats_container.content = ft.Row([
            crear_stat_card("Total Ventas", stats.get('total_ventas', 0), ft.Icons.SHOPPING_CART, DarkTheme.INFO),
            crear_stat_card("Ingresos", f"Q{stats.get('total_ingresos', 0):.2f}", ft.Icons.ATTACH_MONEY, DarkTheme.SUCCESS),
            crear_stat_card("Ganancia", f"Q{stats.get('total_ganancia', 0):.2f}", ft.Icons.TRENDING_UP, DarkTheme.WARNING),
            crear_stat_card("Promedio", f"Q{stats.get('promedio_venta', 0):.2f}", ft.Icons.ANALYTICS, DarkTheme.ACCENT),
        ], spacing=25, wrap=True, alignment=ft.MainAxisAlignment.START)
        
        self.page.update()
    
    def _actualizar_tabla(self):
        """Actualiza la tabla con el historial"""
        self.tabla_filas.controls.clear()
        
        for i, venta in enumerate(self.historial_ventas):
            fila_color = DarkTheme.TABLE_ROW_EVEN if i % 2 == 0 else DarkTheme.TABLE_ROW_ODD
            
            fila = ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(venta['fecha'], color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=160, alignment=ft.alignment.center),
                    ft.Container(ft.Text(venta['id'], color=DarkTheme.ACCENT_TEXT, size=13, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                    ft.Container(ft.Text(venta['producto_nombre'], color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=250, alignment=ft.alignment.center),
                    ft.Container(ft.Text(f"{venta['cantidad_vendida']:.1f} ml", color=DarkTheme.PRIMARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=120, alignment=ft.alignment.center),
                    ft.Container(ft.Text(f"Q{venta['precio_venta']:.2f}", color=DarkTheme.SUCCESS, size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                    ft.Container(ft.Text(f"Q{venta['ganancia']:.2f}", color=DarkTheme.WARNING, size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), width=130, alignment=ft.alignment.center),
                    ft.Container(ft.Text(venta['cliente'], color=DarkTheme.SECONDARY_TEXT, size=13, text_align=ft.TextAlign.CENTER), width=200, alignment=ft.alignment.center),
                ], spacing=15),
                padding=ft.Padding(25, 15, 25, 15),
                bgcolor=fila_color,
                border_radius=8,
                margin=ft.margin.only(bottom=4),
                border=ft.border.all(0.5, DarkTheme.BORDER_COLOR),
                animate_scale=200,
                on_hover=lambda e, container=None: self._on_row_hover(e)
            )
            
            self.tabla_filas.controls.append(fila)
        
        if not self.historial_ventas:
            self.tabla_filas.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.HISTORY, size=64, color=DarkTheme.SECONDARY_TEXT),
                        ft.Text(
                            "No hay ventas registradas",
                            color=DarkTheme.SECONDARY_TEXT,
                            size=18,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        ),
                        ft.Text(
                            "Las ventas aparecerán aquí una vez que registres la primera",
                            color=DarkTheme.MUTED_TEXT,
                            size=14,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(25, 60, 25, 60),
                    alignment=ft.alignment.center
                )
            )
        
        self.page.update()
    
    def _on_row_hover(self, e):
        """Maneja el hover sobre las filas"""
        if e.data == "true":
            e.control.scale = 1.02
        else:
            e.control.scale = 1.0
        e.control.update()
    
    def _filtrar_historial(self, e):
        """Filtra el historial por nombre de producto"""
        filtro = e.control.value.lower() if e.control.value else ""
        
        if not filtro:
            # Mostrar todos
            self._actualizar_tabla()
            return
        
        # Filtrar por nombre de producto
        historial_filtrado = [
            venta for venta in self.historial_ventas
            if filtro in venta['producto_nombre'].lower()
        ]
        
        # Actualizar tabla con datos filtrados
        self.tabla_filas.controls.clear()
        
        for i, venta in enumerate(historial_filtrado):
            fila_color = DarkTheme.TABLE_ROW_EVEN if i % 2 == 0 else DarkTheme.TABLE_ROW_ODD
            
            fila = ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(venta['fecha'], color=DarkTheme.PRIMARY_TEXT, size=13), width=160),
                    ft.Container(ft.Text(venta['id'], color=DarkTheme.ACCENT_TEXT, size=13, weight=ft.FontWeight.W_500), width=120),
                    ft.Container(ft.Text(venta['producto_nombre'], color=DarkTheme.PRIMARY_TEXT, size=13), width=250),
                    ft.Container(ft.Text(f"{venta['cantidad_vendida']:.1f} ml", color=DarkTheme.PRIMARY_TEXT, size=13), width=120),
                    ft.Container(ft.Text(f"Q{venta['precio_venta']:.2f}", color=DarkTheme.SUCCESS, size=13, weight=ft.FontWeight.BOLD), width=130),
                    ft.Container(ft.Text(f"Q{venta['ganancia']:.2f}", color=DarkTheme.WARNING, size=13, weight=ft.FontWeight.BOLD), width=130),
                    ft.Container(ft.Text(venta['cliente'], color=DarkTheme.SECONDARY_TEXT, size=13), width=200),
                ], spacing=15),
                padding=ft.Padding(25, 15, 25, 15),
                bgcolor=fila_color,
                border_radius=8,
                margin=ft.margin.only(bottom=4),
                border=ft.border.all(0.5, DarkTheme.BORDER_COLOR),
                animate_scale=200,
                on_hover=lambda e, container=None: self._on_row_hover(e)
            )
            
            self.tabla_filas.controls.append(fila)
        
        self.page.update()
    
    def _actualizar_datos(self, e):
        """Actualiza todos los datos"""
        self._cargar_datos()
        self.alert_manager.show_toast("Datos actualizados", "info")
    
    def _volver(self, e):
        """Vuelve a la ventana principal"""
        if self.original_content:
            self.page.clean()
            for control in self.original_content:
                self.page.add(control)
            self.page.update()
    
    def show(self):
        """Muestra la ventana del historial"""
        # Guardar el contenido original
        self.original_content = self.page.controls.copy()
        
        # Limpiar la página y mostrar el historial
        self.page.clean()
        self.page.add(self.main_container)
        self.page.update()
