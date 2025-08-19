from typing import List, Optional
from datetime import datetime, date
from utils.database import Producto, create_tables, get_session
from sqlalchemy.exc import SQLAlchemyError

class ProductoService:
    """Servicio para manejar todas las operaciones CRUD de productos"""
    
    def __init__(self):
        # Crear las tablas si no existen
        create_tables()
    
    def agregar_producto(self, id_producto: str, nombre: str, stock_actual: float, 
                        costo_entrada: float, proveedor: str, fecha_caducidad: str, 
                        costo_por_ml: float) -> bool:
        """
        Agrega un nuevo producto a la base de datos
        
        Args:
            id_producto: ID único del producto
            nombre: Nombre de la esencia
            stock_actual: Stock actual en ml
            costo_entrada: Costo total de entrada del producto
            proveedor: Nombre del proveedor
            fecha_caducidad: Fecha en formato YYYY-MM-DD
            costo_por_ml: Costo por mililitro
            
        Returns:
            bool: True si se agregó exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            # Verificar si ya existe un producto con este ID
            if self.buscar_por_id(id_producto):
                raise ValueError(f"Ya existe un producto con ID: {id_producto}")
            
            # Convertir fecha string a date object
            fecha_obj = datetime.strptime(fecha_caducidad, '%Y-%m-%d').date()
            
            nuevo_producto = Producto(
                id=id_producto,
                nombre=nombre,
                stock_actual=int(stock_actual),
                costo_entrada=float(costo_entrada),
                proveedor=proveedor,
                fecha_caducidad=fecha_obj,
                costo_por_ml=float(costo_por_ml)
            )
            
            session.add(nuevo_producto)
            session.commit()
            return True
            
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            print(f"Error al agregar producto: {e}")
            return False
        finally:
            session.close()
    
    def obtener_todos_los_productos(self) -> List[dict]:
        """
        Obtiene todos los productos de la base de datos
        
        Returns:
            List[dict]: Lista de productos como diccionarios
        """
        session = get_session()
        try:
            productos = session.query(Producto).all()
            resultado = []
            
            for producto in productos:
                resultado.append({
                    'id_producto': producto.id,
                    'nombre': producto.nombre,
                    'stock_actual': producto.stock_actual,
                    'costo_entrada': producto.costo_entrada,
                    'proveedor': producto.proveedor,
                    'fecha_caducidad': producto.fecha_caducidad.strftime('%Y-%m-%d'),
                    'costo_por_ml': producto.costo_por_ml,
                    'valor_total': producto.valor_total_stock(),
                    'stock_bajo': producto.stock_bajo()
                })
            
            return resultado
            
        except SQLAlchemyError as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            session.close()
    
    def buscar_por_id(self, id_producto: str) -> Optional[dict]:
        """
        Busca un producto por su ID
        
        Args:
            id_producto: ID del producto a buscar
            
        Returns:
            dict o None: Datos del producto si existe, None si no existe
        """
        session = get_session()
        try:
            producto = session.query(Producto).filter(Producto.id == id_producto).first()
            
            if producto:
                return {
                    'id_producto': producto.id,
                    'nombre': producto.nombre,
                    'stock_actual': producto.stock_actual,
                    'costo_entrada': producto.costo_entrada,
                    'proveedor': producto.proveedor,
                    'fecha_caducidad': producto.fecha_caducidad.strftime('%Y-%m-%d'),
                    'costo_por_ml': producto.costo_por_ml,
                    'valor_total': producto.valor_total_stock(),
                    'stock_bajo': producto.stock_bajo()
                }
            return None
            
        except SQLAlchemyError as e:
            print(f"Error al buscar producto: {e}")
            return None
        finally:
            session.close()
    
    def actualizar_producto(self, id_producto: str, nombre: str, stock_actual: float,
                           costo_entrada: float, proveedor: str, fecha_caducidad: str,
                           costo_por_ml: float) -> bool:
        """
        Actualiza un producto existente
        
        Args:
            id_producto: ID del producto a actualizar
            nombre: Nuevo nombre
            stock_actual: Nuevo stock actual
            costo_entrada: Nuevo costo de entrada
            proveedor: Nuevo proveedor
            fecha_caducidad: Nueva fecha de caducidad
            costo_por_ml: Nuevo costo por ml
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            producto = session.query(Producto).filter(Producto.id == id_producto).first()
            
            if not producto:
                raise ValueError(f"No existe un producto con ID: {id_producto}")
            
            # Convertir fecha string a date object
            fecha_obj = datetime.strptime(fecha_caducidad, '%Y-%m-%d').date()
            
            # Actualizar campos
            producto.nombre = nombre
            producto.stock_actual = int(stock_actual)
            producto.costo_entrada = float(costo_entrada)
            producto.proveedor = proveedor
            producto.fecha_caducidad = fecha_obj
            producto.costo_por_ml = float(costo_por_ml)
            
            session.commit()
            return True
            
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            session.close()
    
    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto de la base de datos
        
        Args:
            id_producto: ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            producto = session.query(Producto).filter(Producto.id == id_producto).first()
            
            if not producto:
                raise ValueError(f"No existe un producto con ID: {id_producto}")
            
            session.delete(producto)
            session.commit()
            return True
            
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            session.close()
    
    def buscar_productos(self, termino: str) -> List[dict]:
        """
        Busca productos por nombre o proveedor
        
        Args:
            termino: Término de búsqueda
            
        Returns:
            List[dict]: Lista de productos que coinciden con la búsqueda
        """
        session = get_session()
        try:
            productos = session.query(Producto).filter(
                (Producto.nombre.contains(termino)) |
                (Producto.proveedor.contains(termino)) |
                (Producto.id.contains(termino))
            ).all()
            
            resultado = []
            for producto in productos:
                resultado.append({
                    'id_producto': producto.id,
                    'nombre': producto.nombre,
                    'stock_actual': producto.stock_actual,
                    'costo_entrada': producto.costo_entrada,
                    'proveedor': producto.proveedor,
                    'fecha_caducidad': producto.fecha_caducidad.strftime('%Y-%m-%d'),
                    'costo_por_ml': producto.costo_por_ml,
                    'valor_total': producto.valor_total_stock(),
                    'stock_bajo': producto.stock_bajo()
                })
            
            return resultado
            
        except SQLAlchemyError as e:
            print(f"Error al buscar productos: {e}")
            return []
        finally:
            session.close()
    
    def obtener_productos_stock_bajo(self) -> List[dict]:
        """
        Obtiene productos con stock bajo
        
        Returns:
            List[dict]: Lista de productos con stock bajo
        """
        productos = self.obtener_todos_los_productos()
        return [p for p in productos if p['stock_bajo']]
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del inventario
        
        Returns:
            dict: Estadísticas del inventario
        """
        productos = self.obtener_todos_los_productos()
        
        total_productos = len(productos)
        productos_stock_bajo = len([p for p in productos if p['stock_bajo']])
        valor_total_inventario = sum(p['valor_total'] for p in productos)
        
        return {
            'total_productos': total_productos,
            'productos_stock_bajo': productos_stock_bajo,
            'valor_total_inventario': valor_total_inventario
        }
    
    def agregar_datos_ejemplo(self):
        """Agrega algunos datos de ejemplo para probar"""
        productos_ejemplo = [
            {
                'id_producto': 'ESE001',
                'nombre': 'Lavanda Premium',
                'stock_actual': 500,
                'costo_entrada': 125.00,
                'proveedor': 'Aromática Natural',
                'fecha_caducidad': '2025-12-31',
                'costo_por_ml': 0.25
            },
            {
                'id_producto': 'ESE002',
                'nombre': 'Rosa Búlgara',
                'stock_actual': 50,
                'costo_entrada': 40.00,
                'proveedor': 'Esencias del Mundo',
                'fecha_caducidad': '2025-06-15',
                'costo_por_ml': 0.80
            },
            {
                'id_producto': 'ESE003',
                'nombre': 'Eucalipto',
                'stock_actual': 300,
                'costo_entrada': 45.00,
                'proveedor': 'Aromática Natural',
                'fecha_caducidad': '2026-03-20',
                'costo_por_ml': 0.15
            },
            {
                'id_producto': 'ESE004',
                'nombre': 'Ylang Ylang',
                'stock_actual': 80,
                'costo_entrada': 76.00,
                'proveedor': 'Tropical Scents',
                'fecha_caducidad': '2025-09-10',
                'costo_por_ml': 0.95
            },
            {
                'id_producto': 'ESE101',
                'nombre': 'Es Davo',
                'stock_actual': 250,
                'costo_entrada': 2500.00,
                'proveedor': 'Luisito',
                'fecha_caducidad': '2025-09-21',
                'costo_por_ml': 10.00
            }
        ]
        
        for producto in productos_ejemplo:
            if not self.buscar_por_id(producto['id_producto']):
                self.agregar_producto(**producto)
