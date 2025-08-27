from typing import List, Optional
from datetime import datetime
from utils.database import Frasco, create_tables, get_session
from sqlalchemy.exc import SQLAlchemyError

class FrascoService:
    """Servicio para manejar todas las operaciones CRUD de frascos"""
    
    def __init__(self):
        # Crear las tablas si no existen
        create_tables()
        self.get_session = get_session
    
    def agregar_frasco(self, id_frasco: str, nombre: str, costo: float, capacidad_ml: float, stock_actual: int = 0) -> bool:
        """
        Agrega un nuevo frasco a la base de datos
        
        Args:
            id_frasco: ID único del frasco
            nombre: Nombre del frasco
            costo: Costo unitario del frasco
            capacidad_ml: Capacidad en mililitros
            stock_actual: Cantidad inicial de frascos
            
        Returns:
            bool: True si se agregó exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            # Verificar si ya existe un frasco con este ID
            if self.buscar_por_id(id_frasco):
                raise ValueError(f"Ya existe un frasco con ID: {id_frasco}")
            
            nuevo_frasco = Frasco(
                id=id_frasco,
                nombre=nombre,
                costo=float(costo),
                capacidad_ml=float(capacidad_ml),
                stock_actual=int(stock_actual)
            )
            
            session.add(nuevo_frasco)
            session.commit()
            return True
            
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            print(f"Error al agregar frasco: {e}")
            return False
        finally:
            session.close()
    
    def obtener_todos_los_frascos(self) -> List[dict]:
        """
        Obtiene todos los frascos de la base de datos
        
        Returns:
            List[dict]: Lista de frascos como diccionarios
        """
        session = get_session()
        try:
            frascos = session.query(Frasco).all()
            resultado = []
            
            for frasco in frascos:
                resultado.append({
                    'id_frasco': frasco.id,
                    'nombre': frasco.nombre,
                    'costo': frasco.costo,
                    'capacidad_ml': frasco.capacidad_ml,
                    'stock_actual': frasco.stock_actual,
                    'valor_total': frasco.valor_total_stock(),
                    'stock_bajo': frasco.stock_bajo(),
                    'tipo_producto': 'frasco'
                })
            
            return resultado
            
        except SQLAlchemyError as e:
            print(f"Error al obtener frascos: {e}")
            return []
        finally:
            session.close()
    
    def buscar_por_id(self, id_frasco: str) -> Optional[dict]:
        """
        Busca un frasco por su ID
        
        Args:
            id_frasco: ID del frasco a buscar
            
        Returns:
            dict o None: Datos del frasco si existe, None si no existe
        """
        session = get_session()
        try:
            frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
            
            if frasco:
                return {
                    'id_frasco': frasco.id,
                    'nombre': frasco.nombre,
                    'costo': frasco.costo,
                    'capacidad_ml': frasco.capacidad_ml,
                    'stock_actual': frasco.stock_actual,
                    'valor_total': frasco.valor_total_stock(),
                    'stock_bajo': frasco.stock_bajo(),
                    'tipo_producto': 'frasco'
                }
            return None
            
        except SQLAlchemyError as e:
            print(f"Error al buscar frasco: {e}")
            return None
        finally:
            session.close()
    
    def actualizar_frasco(self, id_frasco: str, nombre: str, costo: float, capacidad_ml: float, stock_actual: int) -> bool:
        """
        Actualiza un frasco existente
        
        Args:
            id_frasco: ID del frasco a actualizar
            nombre: Nuevo nombre
            costo: Nuevo costo
            capacidad_ml: Nueva capacidad
            stock_actual: Nuevo stock
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
            
            if not frasco:
                print(f"No existe un frasco con ID: {id_frasco}")
                return False
            
            # Actualizar campos
            frasco.nombre = nombre
            frasco.costo = float(costo)
            frasco.capacidad_ml = float(capacidad_ml)
            frasco.stock_actual = int(stock_actual)
            
            session.commit()
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al actualizar frasco: {e}")
            return False
        finally:
            session.close()
    
    def eliminar_frasco(self, id_frasco: str) -> bool:
        """
        Elimina un frasco de la base de datos
        
        Args:
            id_frasco: ID del frasco a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
            
            if not frasco:
                print(f"No existe un frasco con ID: {id_frasco}")
                return False
            
            session.delete(frasco)
            session.commit()
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al eliminar frasco: {e}")
            return False
        finally:
            session.close()
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de los frascos
        
        Returns:
            dict: Estadísticas de frascos
        """
        session = get_session()
        try:
            frascos = session.query(Frasco).all()
            
            total_frascos = len(frascos)
            frascos_stock_bajo = sum(1 for f in frascos if f.stock_bajo())
            valor_total_inventario = sum(f.valor_total_stock() for f in frascos)
            
            return {
                'total_frascos': total_frascos,
                'frascos_stock_bajo': frascos_stock_bajo,
                'valor_total_inventario': valor_total_inventario
            }
            
        except SQLAlchemyError as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_frascos': 0,
                'frascos_stock_bajo': 0,
                'valor_total_inventario': 0.0
            }
        finally:
            session.close()
