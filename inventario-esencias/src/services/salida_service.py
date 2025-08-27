from typing import List, Optional
from datetime import datetime
from utils.database import Salida, Producto, Frasco, get_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

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
    
    def registrar_venta_combinada(self, id_producto: str, id_frasco: str, cantidad_vendida: float, 
                                precio_venta: float, cliente: str = None) -> bool:
        """
        Registra una nueva venta combinada (esencia + frasco)
        
        Args:
            id_producto: ID de la esencia vendida
            id_frasco: ID del frasco vendido
            cantidad_vendida: Cantidad de esencia vendida en ml
            precio_venta: Precio total de la venta
            cliente: Nombre del cliente (opcional)
            
        Returns:
            bool: True si se registró exitosamente, False en caso contrario
        """
        session = get_session()
        try:
            # Verificar que la esencia existe
            producto = session.query(Producto).filter(Producto.id == id_producto).first()
            if not producto:
                raise ValueError(f"No existe una esencia con ID: {id_producto}")
            
            # Verificar que el frasco existe
            frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
            if not frasco:
                raise ValueError(f"No existe un frasco con ID: {id_frasco}")
            
            # Verificar que hay suficiente stock de esencia
            if producto.stock_actual < cantidad_vendida:
                raise ValueError(f"Stock insuficiente de esencia. Disponible: {producto.stock_actual} ml, Solicitado: {cantidad_vendida} ml")
            
            # Verificar que hay suficiente stock de frasco
            if frasco.stock_actual < 1:
                raise ValueError(f"Stock insuficiente de frascos. Disponible: {frasco.stock_actual}, Solicitado: 1")
            
            # Verificar que la cantidad de esencia no excede la capacidad del frasco
            if cantidad_vendida > frasco.capacidad_ml:
                raise ValueError(f"La cantidad de esencia ({cantidad_vendida} ml) excede la capacidad del frasco ({frasco.capacidad_ml} ml)")
            
            # Calcular ganancia combinada
            stock_inicial = producto.stock_actual + cantidad_vendida  # Stock antes de la venta
            costo_por_ml_real = producto.costo_entrada / stock_inicial if stock_inicial > 0 else 0
            costo_esencia = costo_por_ml_real * cantidad_vendida
            costo_frasco = frasco.costo
            costo_alcohol = 2.50  # Costo estándar del alcohol
            costo_total = costo_esencia + costo_frasco + costo_alcohol
            ganancia = precio_venta - costo_total
            
            # Generar ID único para la salida
            id_salida = self._generar_id_salida()
            
            # Crear registro de salida (incluye información del frasco en el cliente field para tracking)
            cliente_info = f"{cliente or 'Cliente general'} | Frasco: {frasco.nombre} ({frasco.capacidad_ml}ml)"
            
            nueva_salida = Salida(
                id=id_salida,
                id_producto=id_producto,
                cantidad_vendida=cantidad_vendida,
                precio_venta=precio_venta,
                fecha_venta=datetime.now(),
                cliente=cliente_info,
                ganancia=ganancia
            )
            
            # Actualizar stock de la esencia
            producto.stock_actual -= cantidad_vendida
            
            # Actualizar stock del frasco
            frasco.stock_actual -= 1
            
            session.add(nueva_salida)
            session.commit()
            return True
            
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            print(f"Error al registrar venta combinada: {e}")
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
                
                # Mostrar TODAS las ventas, incluso de productos eliminados
                if producto:
                    # Producto aún existe en inventario
                    producto_nombre = producto.nombre
                    estado_producto = "Disponible"
                else:
                    # Producto eliminado del inventario - mantener el nombre original
                    producto_nombre = self._recuperar_nombre_producto_eliminado(salida.id_producto)
                    estado_producto = "Sin stock"
                
                # Extraer información del frasco del campo cliente
                cliente_original = salida.cliente or "N/A"
                frasco_nombre = "Sin frasco"
                costo_frasco = 0.0
                
                # Si el cliente contiene información del frasco (formato: "cliente | Frasco: nombre (capacidad)")
                if " | Frasco: " in cliente_original:
                    partes = cliente_original.split(" | Frasco: ")
                    cliente_real = partes[0]
                    frasco_info = partes[1] if len(partes) > 1 else ""
                    
                    # Extraer solo el nombre del frasco (antes del paréntesis)
                    if "(" in frasco_info:
                        frasco_nombre = frasco_info.split("(")[0].strip()
                    else:
                        frasco_nombre = frasco_info
                    
                    # Buscar el costo del frasco
                    frasco = session.query(Frasco).filter(Frasco.nombre == frasco_nombre).first()
                    if frasco:
                        costo_frasco = frasco.costo
                else:
                    cliente_real = cliente_original
                
                # Calcular costo de producción
                costo_esencia = 0.0
                if producto:
                    # Para productos existentes, calcular el stock inicial
                    # sumando el stock actual + todas las ventas de ese producto
                    ventas_totales = session.query(Salida).filter(Salida.id_producto == producto.id).with_entities(
                        func.sum(Salida.cantidad_vendida)
                    ).scalar() or 0
                    stock_inicial_calculado = producto.stock_actual + ventas_totales
                    
                    costo_por_ml = producto.costo_entrada / stock_inicial_calculado if stock_inicial_calculado > 0 else 0
                    costo_esencia = costo_por_ml * salida.cantidad_vendida
                else:
                    # Para productos eliminados, estimar basándose en ganancia
                    # costo_produccion ≈ precio_venta - ganancia
                    costo_esencia = max(0, salida.precio_venta - salida.ganancia - costo_frasco)
                
                # Calcular costo total de producción (estimado para alcohol: Q2.50 por venta)
                costo_alcohol = 2.50  # Estimación fija
                costo_produccion = costo_esencia + costo_alcohol + costo_frasco
                
                # Recalcular ganancia basándose en el costo de producción actual
                ganancia_actual = salida.precio_venta - costo_produccion
                
                historial.append({
                    'id': salida.id,
                    'fecha': salida.fecha_venta.strftime("%d/%m/%Y %H:%M"),
                    'fecha_orden': salida.fecha_venta,  # Para ordenamiento
                    'producto_nombre': producto_nombre,
                    'frasco_nombre': frasco_nombre,
                    'producto_id': salida.id_producto,
                    'cantidad_vendida': salida.cantidad_vendida,
                    'precio_venta': salida.precio_venta,
                    'costo_produccion': costo_produccion,
                    'ganancia': ganancia_actual,
                    'cliente': cliente_real,
                    'estado_producto': estado_producto
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
    
    def _recuperar_nombre_producto_eliminado(self, id_producto):
        """
        Intenta recuperar el nombre original de un producto eliminado
        Basándose en patrones de ID o usando un mapeo de nombres conocidos
        """
        # Mapeo de IDs conocidos a nombres (puedes expandir esto)
        nombres_conocidos = {
            'RILEYREID': 'Riley Reid Essence',
            'ESE001': 'Lavanda Premium',
            'ESE002': 'Rosa Búlgara',
            'ESE003': 'Vainilla Exótica',
            'ESE004': 'Ylang Ylang',
            # Agregar más según sea necesario
        }
        
        # Si el ID está en el mapeo, usar ese nombre
        if id_producto in nombres_conocidos:
            return nombres_conocidos[id_producto]
        
        # Si es un patrón ESE + número, crear nombre genérico
        if id_producto.startswith('ESE'):
            return f"Esencia {id_producto}"
        
        # Para otros casos, usar un nombre descriptivo
        return f"Producto {id_producto}"
