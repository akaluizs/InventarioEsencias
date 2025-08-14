import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from views.main_window import MainWindow
from services.producto_service import ProductoService

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Inventario de Esencias"
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 800
    page.window_min_height = 600
    
    # Crear el servicio de productos
    producto_service = ProductoService()
    
    # Agregar datos de ejemplo si la base de datos está vacía
    if not producto_service.obtener_todos_los_productos():
        producto_service.agregar_datos_ejemplo()
    
    # Crear la ventana principal
    main_window = MainWindow(page)
    
    # Funciones que conectan la UI con la base de datos
    def agregar_producto(id_prod, nombre, stock_actual, stock_minimo, proveedor, fecha_cad, costo_ml):
        success = producto_service.agregar_producto(
            id_prod, nombre, stock_actual, stock_minimo, 
            proveedor, fecha_cad, costo_ml
        )
        if success:
            productos = producto_service.obtener_todos_los_productos()
            main_window.mostrar_productos(productos)
        else:
            raise Exception("No se pudo agregar el producto")
    
    def actualizar_producto(id_prod, nombre, stock_actual, stock_minimo, proveedor, fecha_cad, costo_ml):
        success = producto_service.actualizar_producto(
            id_prod, nombre, stock_actual, stock_minimo,
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
    
    # Configurar callbacks
    main_window.set_callbacks(agregar_producto, actualizar_producto, eliminar_producto, cargar_productos)

ft.app(target=main)