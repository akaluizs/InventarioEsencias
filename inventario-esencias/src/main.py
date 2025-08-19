import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from views.main_window import MainWindow
from views.salidas_form_window import SalidasFormWindow
from views.historial_ventas_window import HistorialVentasWindow
from services.producto_service import ProductoService
from services.salida_service import SalidaService

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Inventario de Esencias 🧪"
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 800
    page.window_min_height = 600
    
    # Configurar icono de la aplicación usando un icono Material
    page.window_title_bar_hidden = False
    page.window_title_bar_buttons_hidden = False
    
    # Configurar tema oscuro
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.GREY_900
    
    # Configurar icono de la aplicación con ruta absoluta
    import os
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(current_dir, "assets", "icono.ico")
    print(f"DEBUG: Buscando icono ICO en: {icon_path}")
    print(f"DEBUG: ¿Existe el archivo ICO? {os.path.exists(icon_path)}")
    
    if os.path.exists(icon_path):
        page.window_icon = icon_path
        print(f"DEBUG: Icono ICO configurado: {icon_path}")
    else:
        print("DEBUG: No se encontró el icono ICO, usando icono por defecto")
    
    # Crear los servicios
    producto_service = ProductoService()
    salida_service = SalidaService()
    
    # Agregar datos de ejemplo si la base de datos está vacía
    if not producto_service.obtener_todos_los_productos():
        producto_service.agregar_datos_ejemplo()
    
    # Crear la ventana principal
    main_window = MainWindow(page)
    
    # Funciones que conectan la UI con la base de datos
    def agregar_producto(id_prod, nombre, stock_actual, costo_entrada, proveedor, fecha_cad, costo_ml):
        success = producto_service.agregar_producto(
            id_prod, nombre, stock_actual, costo_entrada, 
            proveedor, fecha_cad, costo_ml
        )
        if success:
            productos = producto_service.obtener_todos_los_productos()
            main_window.mostrar_productos(productos)
        else:
            raise Exception("No se pudo agregar el producto")
    
    def actualizar_producto(id_prod, nombre, stock_actual, costo_entrada, proveedor, fecha_cad, costo_ml):
        success = producto_service.actualizar_producto(
            id_prod, nombre, stock_actual, costo_entrada,
            proveedor, fecha_cad, costo_ml
        )
        if success:
            productos = producto_service.obtener_todos_los_productos()
            main_window.mostrar_productos(productos)
        else:
            raise Exception("No se pudo actualizar el producto")
    
    def eliminar_producto(id_prod):
        success = producto_service.eliminar_producto(id_prod)
        if success:
            productos = producto_service.obtener_todos_los_productos()
            main_window.mostrar_productos(productos)
        else:
            raise Exception("No se pudo eliminar el producto")
    
    def cargar_productos():
        productos = producto_service.obtener_todos_los_productos()
        main_window.mostrar_productos(productos)
    
    def mostrar_form_salidas():
        # Obtener productos disponibles
        productos = producto_service.obtener_todos_los_productos()
        
        # Crear ventana de salidas
        salidas_window = SalidasFormWindow(page, productos)
        
        # Configurar el callback de guardado
        def on_save_salida(data):
            try:
                # Registrar la salida usando el servicio
                salida_service.registrar_salida(
                    data['producto_id'],
                    data['cantidad'],
                    data['precio_venta'],
                    data.get('cliente')
                )
                
                # Actualizar la lista de productos en la ventana principal
                productos_actualizados = producto_service.obtener_todos_los_productos()
                main_window.mostrar_productos(productos_actualizados)
                
                # Mostrar alerta de éxito
                main_window.alert_manager.show_success("¡Venta registrada exitosamente!")
                
                return True
            except Exception as e:
                # Mostrar alerta de error
                main_window.alert_manager.show_error(f"Error al registrar venta: {str(e)}")
                print(f"Error al registrar salida: {e}")
                return False
        
        salidas_window.set_callbacks(on_save=on_save_salida, on_cancel=None)
        salidas_window.show()
    
    def mostrar_historial_ventas():
        # Crear ventana de historial
        historial_window = HistorialVentasWindow(page, salida_service, producto_service)
        historial_window.show()
    
    # Configurar callbacks
    main_window.set_callbacks(agregar_producto, actualizar_producto, eliminar_producto, cargar_productos, mostrar_form_salidas, mostrar_historial_ventas)

ft.app(target=main)