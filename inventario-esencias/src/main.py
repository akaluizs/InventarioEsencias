import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from views.main_window import MainWindow
from views.salidas_form_window import SalidasFormWindow
from views.historial_ventas_window import HistorialVentasWindow
from services.producto_service import ProductoService
from services.salida_service import SalidaService
from services.frasco_service import FrascoService

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
    frasco_service = FrascoService()
    
    # Agregar datos de ejemplo si la base de datos está vacía
    # if not producto_service.obtener_todos_los_productos():
    #     producto_service.agregar_datos_ejemplo()
    
    # Crear la ventana principal
    main_window = MainWindow(page)
    
    # Funciones que conectan la UI con la base de datos
    def agregar_producto(id_prod, nombre, genero, stock_actual, costo_entrada, proveedor, fecha_cad, costo_ml):
        success = producto_service.agregar_producto(
            id_prod, nombre, stock_actual, costo_entrada, 
            proveedor, fecha_cad, costo_ml, genero
        )
        if success:
            cargar_productos()  # Usar cargar_productos para incluir frascos
        else:
            raise Exception("No se pudo agregar el producto")
    
    def actualizar_producto(id_prod, nombre, genero, stock_actual, costo_entrada, proveedor, fecha_cad, costo_ml):
        success = producto_service.actualizar_producto(
            id_prod, nombre, genero, stock_actual, costo_entrada, 
            proveedor, fecha_cad, costo_ml
        )
        if success:
            cargar_productos()  # Usar cargar_productos para incluir frascos
        else:
            raise Exception("No se pudo actualizar el producto")
    
    def eliminar_producto(id_prod):
        try:
            # Detectar tipo de producto por prefijo en el ID
            if "F" in id_prod.upper():
                # Es un frasco, usar frasco_service
                success = frasco_service.eliminar_frasco(id_prod)
                tipo_producto = "frasco"
            elif "ESE" in id_prod.upper():
                # Es una esencia, usar producto_service
                success = producto_service.eliminar_producto(id_prod)
                tipo_producto = "esencia"
            else:
                # Por defecto, intentar como esencia primero, luego como frasco
                success = producto_service.eliminar_producto(id_prod)
                if not success:
                    success = frasco_service.eliminar_frasco(id_prod)
                    tipo_producto = "frasco" if success else "producto"
                else:
                    tipo_producto = "esencia"
            
            if success:
                cargar_productos()  # Usar cargar_productos para incluir frascos
                return True
            else:
                # Crear un mensaje más específico
                raise ValueError(f"No se encontró el {tipo_producto} con ID '{id_prod}' en la base de datos")
        except Exception as e:
            # Propagar la excepción con el mensaje específico del servicio
            raise e
    
    def cargar_productos():
        # Obtener esencias
        esencias = producto_service.obtener_todos_los_productos()
        print(f"DEBUG: Esencias cargadas: {len(esencias)}")
        
        # Obtener frascos y convertirlos al formato de productos
        frascos = frasco_service.obtener_todos_los_frascos()
        print(f"DEBUG: Frascos cargados: {len(frascos)}")
        frascos_formateados = []
        
        for frasco in frascos:
            frasco_formateado = {
                'id_producto': frasco.get('id_frasco'),
                'nombre': frasco.get('nombre'),
                'tipo_producto': 'frasco',
                'genero': 'N/A',  # Los frascos no tienen género
                'stock_actual': frasco.get('stock_actual', 0),
                'costo_entrada': frasco.get('costo', 0),  # Usar costo como costo_entrada
                'proveedor': 'N/A',  # Los frascos no tienen proveedor específico
                'fecha_caducidad': 'N/A',  # Los frascos no caducan
                'costo_por_ml': round(frasco.get('costo', 0) / max(frasco.get('capacidad_ml', 1), 1), 4) if frasco.get('capacidad_ml') else 0,
                'capacidad_ml': frasco.get('capacidad_ml', 0),  # Información adicional para frascos
                'costo_frasco': frasco.get('costo', 0)  # Costo por frasco
            }
            frascos_formateados.append(frasco_formateado)
        
        # Combinar esencias y frascos
        todos_productos = esencias + frascos_formateados
        print(f"DEBUG: Total productos combinados: {len(todos_productos)}")
        main_window.mostrar_productos(todos_productos)
    
    def mostrar_form_salidas():
        # Obtener productos disponibles (solo esencias)
        productos = producto_service.obtener_todos_los_productos()
        
        # Obtener frascos disponibles
        frascos = frasco_service.obtener_todos_los_frascos()
        
        # Crear ventana de salidas
        salidas_window = SalidasFormWindow(page, productos, frascos)
        
        # Configurar el callback de guardado
        def on_save_salida(data):
            try:
                # Registrar la venta combinada usando el nuevo servicio
                salida_service.registrar_venta_combinada(
                    data['producto_id'],
                    data['frasco_id'],
                    data['cantidad'],
                    data['precio_venta'],
                    data.get('cliente')
                )
                
                # Actualizar la lista de productos en la ventana principal
                cargar_productos()  # Usar cargar_productos para incluir frascos
                
                # Mostrar alerta de éxito
                main_window.alert_manager.show_success("¡Venta combinada registrada exitosamente!")
                
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
    
    # Funciones para manejar frascos
    def agregar_frasco(id_frasco, nombre, capacidad_ml, stock_actual, costo):
        success = frasco_service.agregar_frasco(
            id_frasco, nombre, capacidad_ml, stock_actual, costo
        )
        if success:
            cargar_productos()  # Usar cargar_productos para incluir frascos
        else:
            raise Exception("No se pudo agregar el frasco")
    
    def actualizar_frasco(id_frasco, nombre, capacidad_ml, stock_actual, costo):
        success = frasco_service.actualizar_frasco(
            id_frasco, nombre, costo, capacidad_ml, stock_actual
        )
        if success:
            cargar_productos()  # Usar cargar_productos para incluir frascos
        else:
            raise Exception("No se pudo actualizar el frasco")
    
    # Configurar callbacks
    main_window.set_callbacks(
        agregar_producto, 
        actualizar_producto, 
        eliminar_producto, 
        cargar_productos, 
        mostrar_form_salidas, 
        mostrar_historial_ventas,
        agregar_frasco,
        actualizar_frasco
    )
    
    # Cargar productos iniciales (esencias + frascos)
    cargar_productos()

ft.app(target=main)