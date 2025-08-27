"""
Utilidades para gestionar el historial independiente
"""
import sqlite3
import os

def verificar_productos_huerfanos():
    """
    Verifica qué productos en el historial ya no existen en el inventario
    Útil para auditoría y limpieza
    """
    
    # Buscar la base de datos
    possible_paths = [
        'inventario.db',
        '../inventario.db',
        os.path.join(os.path.dirname(__file__), '..', 'inventario.db'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'inventario.db')
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("No se encontró la base de datos inventario.db")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando productos huérfanos en el historial...")
        
        # Obtener productos únicos del historial que ya no están en inventario
        cursor.execute("""
            SELECT DISTINCT s.id_producto, COUNT(s.id) as ventas
            FROM salidas s
            LEFT JOIN productos p ON s.id_producto = p.id
            WHERE p.id IS NULL
            GROUP BY s.id_producto
            ORDER BY ventas DESC
        """)
        
        huerfanos = cursor.fetchall()
        
        if huerfanos:
            print(f"\n📋 Productos eliminados del inventario con historial:")
            print("-" * 50)
            for producto_id, num_ventas in huerfanos:
                print(f"   {producto_id}: {num_ventas} venta(s) registrada(s)")
            
            print(f"\n✅ Total: {len(huerfanos)} productos eliminados")
            print("💡 El historial se mantiene para auditoría y contabilidad")
        else:
            print("✅ No hay productos huérfanos en el historial")
            print("   Todos los productos del historial aún existen en inventario")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al verificar productos huérfanos: {str(e)}")

def limpiar_historial_huerfano(producto_id=None):
    """
    Limpia el historial de productos huérfanos (USAR CON CUIDADO)
    Si no se especifica producto_id, limpia TODOS los huérfanos
    """
    print("⚠️  ADVERTENCIA: Esta operación eliminará registros del historial")
    print("   Solo usar si está seguro de que no necesita estos datos")
    
    respuesta = input("¿Está seguro? (escriba 'CONFIRMAR' para continuar): ")
    if respuesta != 'CONFIRMAR':
        print("❌ Operación cancelada")
        return
    
    # Implementar lógica de limpieza si es necesario...
    print("🚧 Función de limpieza no implementada por seguridad")
    print("   Contacte al desarrollador si necesita esta funcionalidad")

if __name__ == "__main__":
    verificar_productos_huerfanos()
