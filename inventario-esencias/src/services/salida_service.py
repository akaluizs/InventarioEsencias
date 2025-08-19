from typing import List, Optional
from datetime import datetime
from utils.database import Salida, Producto, get_session
from sqlalchemy.exc import SQLAlchemyError

class SalidaService:
    """Servicio para manejar todas las operaciones CRUD de salidas"""
    
    def __init__(self):
        pass
    
    def registrar_salida(self, id_producto: str, cantidad_vendida: float, 
                        precio_venta: float, cliente: str = None) -> bool:
        """
        Registra una nueva salida de producto
        
        Args:
            id_producto: ID del producto vendido
            cantidad_vendida: Cantidad vendida en ml
            precio_venta: Precio total de la venta
            cliente: Nombre del cliente (opcional)
            
        Returns:
            bool: True si se registró exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            # Verificar que el producto existe
            producto = session.query(Producto).filter(Producto.id == id_producto).first()
            if not producto:
                raise ValueError(f"No existe un producto con ID: {id_producto}")
            
            # Verificar que hay suficiente stock
            if producto.stock_actual < cantidad_vendida:
                raise ValueError(f"Stock insuficiente. Disponible: {producto.stock_actual} ml, Solicitado: {cantidad_vendida} ml")
            
            # Calcular ganancia
            stock_inicial = producto.stock_actual + cantidad_vendida  # Stock antes de la venta
            costo_por_ml_real = producto.costo_entrada / stock_inicial if stock_inicial > 0 else 0
            costo_total_vendido = costo_por_ml_real * cantidad_vendida
            ganancia = precio_venta - costo_total_vendido
            
            # Generar ID único para la salida
            id_salida = self._generar_id_salida()
            
            # Crear registro de salida
            nueva_salida = Salida(
                id=id_salida,
                id_producto=id_producto,
                cantidad_vendida=cantidad_vendida,
                precio_venta=precio_venta,
                fecha_venta=datetime.now(),
                cliente=cliente or "",
                ganancia=ganancia
            )
            
            # Actualizar stock del producto
            producto.stock_actual -= cantidad_vendida
            
            session.add(nueva_salida)
            session.commit()
            return True
            
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            print(f"Error al registrar salida: {e}")
            raise e
        finally:
            session.close()
    
    def obtener_todas_las_salidas(self) -> List[dict]:
        """
        Obtiene todas las salidas registradas
        
        Returns:
            List[dict]: Lista de diccionarios con información de las salidas
        """
        session = get_session()
        try:
            salidas = session.query(Salida).join(Producto).all()
            resultado = []
            
            for salida in salidas:
                producto = session.query(Producto).filter(Producto.id == salida.id_producto).first()
                resultado.append({
                    'id_salida': salida.id,
                    'id_producto': salida.id_producto,
                    'nombre_producto': producto.nombre if producto else "Producto no encontrado",
                    'cantidad_vendida': salida.cantidad_vendida,
                    'precio_venta': salida.precio_venta,
                    'fecha_venta': salida.fecha_venta.strftime('%Y-%m-%d %H:%M:%S'),
                    'cliente': salida.cliente,
                    'ganancia': salida.ganancia
                })
            
            return resultado
            
        except SQLAlchemyError as e:
            print(f"Error al obtener salidas: {e}")
            return []
        finally:
            session.close()
    
    def obtener_salidas_por_producto(self, id_producto: str) -> List[dict]:
        """
        Obtiene todas las salidas de un producto específico
        
        Args:
            id_producto: ID del producto
            
        Returns:
            List[dict]: Lista de salidas del producto
        """
        session = get_session()
        try:
            salidas = session.query(Salida).filter(Salida.id_producto == id_producto).all()
            resultado = []
            
            for salida in salidas:
                resultado.append({
                    'id_salida': salida.id,
                    'cantidad_vendida': salida.cantidad_vendida,
                    'precio_venta': salida.precio_venta,
                    'fecha_venta': salida.fecha_venta.strftime('%Y-%m-%d %H:%M:%S'),
                    'cliente': salida.cliente,
                    'ganancia': salida.ganancia
                })
            
            return resultado
            
        except SQLAlchemyError as e:
            print(f"Error al obtener salidas del producto: {e}")
            return []
        finally:
            session.close()
    
    def obtener_estadisticas_ventas(self) -> dict:
        """
        Obtiene estadísticas generales de ventas
        
        Returns:
            dict: Diccionario con estadísticas de ventas
        """
        session = get_session()
        try:
            salidas = session.query(Salida).all()
            
            total_ventas = len(salidas)
            total_ingresos = sum(salida.precio_venta for salida in salidas)
            total_ganancias = sum(salida.ganancia for salida in salidas)
            
            return {
                'total_ventas': total_ventas,
                'total_ingresos': total_ingresos,
                'total_ganancias': total_ganancias,
                'ganancia_promedio': total_ganancias / total_ventas if total_ventas > 0 else 0
            }
            
        except SQLAlchemyError as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_ventas': 0,
                'total_ingresos': 0.0,
                'total_ganancias': 0.0,
                'ganancia_promedio': 0.0
            }
        finally:
            session.close()
    
    def _generar_id_salida(self) -> str:
        """Genera un ID único para la salida"""
        session = get_session()
        try:
            # Obtener el último ID
            ultima_salida = session.query(Salida).order_by(Salida.id.desc()).first()
            
            if ultima_salida:
                # Extraer el número del último ID (formato: SAL001, SAL002, etc.)
                ultimo_numero = int(ultima_salida.id[3:])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
            
            return f"SAL{nuevo_numero:03d}"
            
        except Exception:
            # Si hay algún error, usar timestamp
            return f"SAL{int(datetime.now().timestamp())}"
        finally:
            session.close()
    
    def obtener_historial_ventas(self):
        """
        Obtiene el historial completo de ventas
        
        Returns:
            list: Lista de diccionarios con información de las ventas
        """
        session = get_session()
        try:
            # Obtener todas las salidas
            salidas = session.query(Salida).all()
            
            historial = []
            for salida in salidas:
                # Obtener el producto manualmente
                producto = session.query(Producto).filter(Producto.id == salida.id_producto).first()
                
                if producto:
                    historial.append({
                        'id': salida.id,
                        'fecha': salida.fecha_venta.strftime("%d/%m/%Y %H:%M"),
                        'fecha_orden': salida.fecha_venta,  # Para ordenamiento
                        'producto_nombre': producto.nombre,
                        'producto_id': salida.id_producto,
                        'cantidad_vendida': salida.cantidad_vendida,
                        'precio_venta': salida.precio_venta,
                        'ganancia': salida.ganancia,
                        'cliente': salida.cliente or "N/A"
                    })
            
            # Ordenar por fecha descendente (más recientes primero)
            historial.sort(key=lambda x: x['fecha_orden'], reverse=True)
            
            return historial
            
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
        finally:
            session.close()
    
    def obtener_estadisticas_ventas(self):
        """
        Obtiene estadísticas básicas de las ventas
        
        Returns:
            dict: Diccionario con estadísticas de ventas
        """
        session = get_session()
        try:
            salidas = session.query(Salida).all()
            
            if not salidas:
                return {
                    'total_ventas': 0,
                    'total_ingresos': 0.0,
                    'total_ganancia': 0.0,
                    'promedio_venta': 0.0,
                    'productos_vendidos': 0
                }
            
            total_ventas = len(salidas)
            total_ingresos = sum(s.precio_venta for s in salidas)
            total_ganancia = sum(s.ganancia for s in salidas)
            promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
            productos_vendidos = len(set(s.id_producto for s in salidas))
            
            return {
                'total_ventas': total_ventas,
                'total_ingresos': round(total_ingresos, 2),
                'total_ganancia': round(total_ganancia, 2),
                'promedio_venta': round(promedio_venta, 2),
                'productos_vendidos': productos_vendidos
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_ventas': 0,
                'total_ingresos': 0.0,
                'total_ganancia': 0.0,
                'promedio_venta': 0.0,
                'productos_vendidos': 0
            }
        finally:
            session.close()
