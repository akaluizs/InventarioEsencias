"""
Script de prueba para eliminar un producto y verificar el historial
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.producto_service import ProductoService
import sqlite3

def test_eliminacion():
    """Prueba la eliminación de un producto y verifica el historial"""
    
    # Primero verificar estado antes
    print("=" * 50)
    print("🔍 ESTADO ANTES DE LA ELIMINACIÓN")
    print("=" * 50)
    
    # Buscar la base de datos
    possible_paths = [
        'inventario.db',
        '../inventario.db',
        '../../inventario.db'
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ No se encontró la base de datos")
        return
    
    print(f"📁 Usando BD: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ver productos
    cursor.execute("SELECT id, nombre FROM productos")
    productos = cursor.fetchall()
    print(f"\n🧪 PRODUCTOS ({len(productos)}):")
    for prod_id, nombre in productos:
        print(f"   • {prod_id}: {nombre}")
    
    # Ver ventas
    cursor.execute("SELECT id_producto, cantidad_vendida, cliente FROM salidas")
    ventas = cursor.fetchall()
    print(f"\n📊 VENTAS ({len(ventas)}):")
    for id_prod, cantidad, cliente in ventas:
        print(f"   • {id_prod}: {cantidad}ml - {cliente or 'N/A'}")
    
    conn.close()
    
    # Elegir un producto para eliminar
    if productos:
        producto_a_eliminar = productos[0][0]  # Primer producto
        print(f"\n🎯 ELIMINANDO PRODUCTO: {producto_a_eliminar}")
        
        # Usar el servicio para eliminar
        service = ProductoService()
        resultado = service.eliminar_producto(producto_a_eliminar)
        
        print(f"Resultado de eliminación: {resultado}")
        
        # Verificar estado después
        print("\n" + "=" * 50)
        print("🔍 ESTADO DESPUÉS DE LA ELIMINACIÓN")
        print("=" * 50)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ver productos restantes
        cursor.execute("SELECT id, nombre FROM productos")
        productos_restantes = cursor.fetchall()
        print(f"\n🧪 PRODUCTOS RESTANTES ({len(productos_restantes)}):")
        for prod_id, nombre in productos_restantes:
            print(f"   • {prod_id}: {nombre}")
        
        # Ver si las ventas se mantienen
        cursor.execute("SELECT id_producto, cantidad_vendida, cliente FROM salidas")
        ventas_restantes = cursor.fetchall()
        print(f"\n📊 VENTAS RESTANTES ({len(ventas_restantes)}):")
        for id_prod, cantidad, cliente in ventas_restantes:
            print(f"   • {id_prod}: {cantidad}ml - {cliente or 'N/A'}")
        
        # Verificar específicamente las ventas del producto eliminado
        cursor.execute("SELECT COUNT(*) FROM salidas WHERE id_producto = ?", (producto_a_eliminar,))
        ventas_producto_eliminado = cursor.fetchone()[0]
        print(f"\n🎯 VENTAS DEL PRODUCTO ELIMINADO ({producto_a_eliminar}): {ventas_producto_eliminado}")
        
        conn.close()
        
        if ventas_producto_eliminado > 0:
            print("✅ ¡ÉXITO! El historial se mantuvo")
        else:
            print("❌ ERROR: El historial se eliminó también")
    
    else:
        print("❌ No hay productos para eliminar")

if __name__ == "__main__":
    test_eliminacion()
