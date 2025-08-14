import flet as ft
from datetime import datetime
from typing import List, Optional, Callable
from views.producto_form_window import ProductoFormWindow
from utils.alerts import AlertManager

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
        
        # Botones de acción principales
        self.btn_nuevo_producto = ft.ElevatedButton(
            "Nuevo Producto",
            icon=ft.Icons.ADD,
            on_click=self._abrir_formulario_nuevo,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_400,
                color=ft.Colors.WHITE
            ),
            width=180,
            height=50
        )
        
        self.btn_actualizar_lista = ft.ElevatedButton(
            "Actualizar Lista",
            icon=ft.Icons.REFRESH,
            on_click=self._actualizar_lista,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_400,
                color=ft.Colors.WHITE
            ),
            width=180,
            height=50
        )
        
        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar productos...",
            on_change=self._filtrar_productos,
            prefix_icon=ft.Icons.SEARCH,
            width=350,
            height=50
        )
        
        # Filtros
        self.filtro_stock_bajo = ft.Checkbox(
            label="Solo productos con stock bajo",
            on_change=self._filtrar_productos
        )
        
        # DataTable para mostrar productos
        self.tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Stock Actual")),
                ft.DataColumn(ft.Text("Stock Mínimo")),
                ft.DataColumn(ft.Text("Proveedor")),
                ft.DataColumn(ft.Text("Caducidad")),
                ft.DataColumn(ft.Text("Costo/ml")),
                ft.DataColumn(ft.Text("Valor Total")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            heading_row_color=ft.Colors.GREY_100,
        )
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        self.page.title = "Inventario de Esencias"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        
        # Título principal
        titulo = ft.Container(
            content=ft.Text(
                "🌸 Inventario de Esencias 🌸",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PURPLE_700
            ),
            padding=ft.padding.symmetric(vertical=20, horizontal=20)
        )
        
        # Barra de herramientas principal
        toolbar = ft.Container(
            content=ft.Row([
                self.btn_nuevo_producto,
                self.btn_actualizar_lista,
                ft.VerticalDivider(width=20),
                self.search_field,
                self.filtro_stock_bajo,
            ], spacing=15, wrap=True, alignment=ft.MainAxisAlignment.START),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            bgcolor=ft.Colors.BLUE_50,
            margin=ft.margin.symmetric(horizontal=20)
        )
        
        # Sección de estadísticas
        self.stats_container = ft.Container(
            content=self._crear_estadisticas(),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            bgcolor=ft.Colors.GREEN_50,
            margin=ft.margin.symmetric(horizontal=20)
        )
        
        # Sección de tabla con scroll mejorado
        seccion_tabla = ft.Container(
            content=ft.Column([
                ft.Text("Lista de Productos", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=self.tabla_productos,
                            expand=True,
                        )
                    ], scroll=ft.ScrollMode.ADAPTIVE),
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    border_radius=10,
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    height=400,  # Altura fija para activar scroll vertical
                )
            ], spacing=10),
            padding=20,
            margin=ft.margin.symmetric(horizontal=20)
        )
        
        # Layout principal con scroll optimizado
        main_content = ft.Column([
            titulo,
            toolbar,
            self.stats_container,
            seccion_tabla,
        ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        
        # Container principal sin altura fija para permitir scroll natural
        self.page.add(main_content)
        
        # Cargar productos iniciales
        if self.on_cargar_productos:
            self.on_cargar_productos()
    
    def _crear_estadisticas(self):
        """Crea el widget de estadísticas"""
        total_productos = len(self.productos)
        productos_bajo_stock = len([p for p in self.productos if self._necesita_reabastecimiento(p)])
        valor_total_inventario = sum(self._calcular_valor_total(p) for p in self.productos)
        
        return ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Total Productos", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(str(total_productos), size=24, color=ft.Colors.BLUE_700)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=ft.Colors.BLUE_100,
                border_radius=10,
                width=150,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Stock Bajo", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(str(productos_bajo_stock), size=24, color=ft.Colors.RED_700)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=ft.Colors.RED_100,
                border_radius=10,
                width=150,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Valor Total", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(f"${valor_total_inventario:.2f}", size=20, color=ft.Colors.GREEN_700)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=ft.Colors.GREEN_100,
                border_radius=10,
                width=150,
            ),
        ], wrap=True)
    
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
    
    def _actualizar_lista(self, e):
        """Actualiza la lista de productos"""
        if self.on_cargar_productos:
            self.on_cargar_productos()
            self.alert_manager.show_toast("Lista actualizada", "info")
    
    def _on_producto_saved(self, data, is_editing):
        """Maneja cuando se guarda un producto desde el formulario"""
        try:
            if is_editing:
                if self.on_actualizar_producto:
                    self.on_actualizar_producto(
                        data['id_producto'],
                        data['nombre'],
                        data['stock_actual'],
                        data['stock_minimo'],
                        data['proveedor'],
                        data['fecha_caducidad'],
                        data['costo_por_ml']
                    )
                    self.alert_manager.show_success(
                        f"✅ Producto '{data['nombre']}' actualizado correctamente"
                    )
            else:
                if self.on_agregar_producto:
                    self.on_agregar_producto(
                        data['id_producto'],
                        data['nombre'],
                        data['stock_actual'],
                        data['stock_minimo'],
                        data['proveedor'],
                        data['fecha_caducidad'],
                        data['costo_por_ml']
                    )
                    self.alert_manager.show_success(
                        f"🌸 Esencia '{data['nombre']}' agregada correctamente"
                    )
        except Exception as ex:
            action = "actualizar" if is_editing else "agregar"
            self.alert_manager.show_error(
                f"❌ Error al {action} producto: {str(ex)}"
            )
    
    def _mostrar_mensaje(self, mensaje, color):
        """Muestra un mensaje al usuario"""
        snack = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE),
            bgcolor=color,
            action="OK",
            action_color=ft.Colors.WHITE,
        )
        self.page.show_snack_bar(snack)
    
    def _eliminar_producto(self, producto_id):
        """Elimina un producto"""
        if self.on_eliminar_producto:
            try:
                self.on_eliminar_producto(producto_id)
                self.alert_manager.show_success(
                    f"🗑️ Producto '{producto_id}' eliminado correctamente"
                )
            except Exception as ex:
                self.alert_manager.show_error(
                    f"❌ Error al eliminar producto: {str(ex)}"
                )
    
    def _filtrar_productos(self, e=None):
        """Filtra los productos según los criterios"""
        texto_busqueda = self.search_field.value.lower() if self.search_field.value else ""
        solo_stock_bajo = self.filtro_stock_bajo.value
        
        self.productos_filtrados = []
        
        for producto in self.productos:
            # Filtro por texto
            coincide_texto = (
                texto_busqueda in producto['nombre'].lower() or
                texto_busqueda in producto['proveedor'].lower() or
                texto_busqueda in str(producto['id_producto'])
            )
            
            # Filtro por stock bajo
            stock_bajo = self._necesita_reabastecimiento(producto)
            coincide_stock = not solo_stock_bajo or stock_bajo
            
            if coincide_texto and coincide_stock:
                self.productos_filtrados.append(producto)
        
        self._actualizar_tabla()
    
    def _necesita_reabastecimiento(self, producto):
        """Verifica si un producto necesita reabastecimiento"""
        return producto['stock_actual'] < producto['stock_minimo']
    
    def _calcular_valor_total(self, producto):
        """Calcula el valor total del stock de un producto"""
        return producto['stock_actual'] * producto['costo_por_ml']
    
    def _actualizar_tabla(self):
        """Actualiza la tabla de productos"""
        self.tabla_productos.rows.clear()
        
        productos_a_mostrar = self.productos_filtrados if hasattr(self, 'productos_filtrados') else self.productos
        
        for producto in productos_a_mostrar:
            necesita_restock = self._necesita_reabastecimiento(producto)
            valor_total = self._calcular_valor_total(producto)
            
            # Estado del producto
            estado_color = ft.Colors.RED if necesita_restock else ft.Colors.GREEN
            estado_texto = "⚠️ Stock Bajo" if necesita_restock else "✅ OK"
            
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(producto['id_producto']))),
                    ft.DataCell(ft.Text(producto['nombre'])),
                    ft.DataCell(ft.Text(f"{producto['stock_actual']} ml")),
                    ft.DataCell(ft.Text(f"{producto['stock_minimo']} ml")),
                    ft.DataCell(ft.Text(producto['proveedor'])),
                    ft.DataCell(ft.Text(producto['fecha_caducidad'])),
                    ft.DataCell(ft.Text(f"${producto['costo_por_ml']:.2f}")),
                    ft.DataCell(ft.Text(f"${valor_total:.2f}")),
                    ft.DataCell(ft.Text(estado_texto, color=estado_color)),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, p=producto: self._abrir_formulario_editar(p)
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                tooltip="Eliminar",
                                on_click=lambda e, pid=producto['id_producto']: self._confirmar_eliminacion(pid)
                            ),
                        ], tight=True)
                    ),
                ]
            )
            self.tabla_productos.rows.append(row)
        
        # Actualizar estadísticas
        self.stats_container.content = self._crear_estadisticas()
        self.page.update()
    
    def _confirmar_eliminacion(self, producto_id):
        """Muestra diálogo de confirmación para eliminar"""
        # Buscar el nombre del producto para mostrar en la confirmación
        producto_nombre = None
        for producto in self.productos:
            if producto['id_producto'] == producto_id:
                producto_nombre = producto['nombre']
                break
        
        mensaje = f"¿Estás seguro de que quieres eliminar el producto '{producto_nombre or producto_id}'?"
        
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
        self._actualizar_tabla()
    
    def actualizar_tabla(self, productos: List[dict]):
        """Actualiza la tabla con nueva lista de productos"""
        self.mostrar_productos(productos)
    
    def set_callbacks(self, agregar_callback, actualizar_callback, eliminar_callback, cargar_callback):
        """Establece los callbacks para las operaciones"""
        self.on_agregar_producto = agregar_callback
        self.on_actualizar_producto = actualizar_callback
        self.on_eliminar_producto = eliminar_callback
        self.on_cargar_productos = cargar_callback
