"""
Script para verificar el estado actual de la base de datos
"""
import sqlite3
import os

def verificar_estado_bd():
    """Verifica productos y ventas en la base de datos"""
    
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
        
        print("=" * 50)
        print("📋 ESTADO ACTUAL DE LA BASE DE DATOS")
        print("=" * 50)
        
        # Verificar productos
        cursor.execute("SELECT COUNT(*) FROM productos")
        num_productos = cursor.fetchone()[0]
        print(f"\n🧪 PRODUCTOS EN INVENTARIO: {num_productos}")
        
        if num_productos > 0:
            cursor.execute("SELECT id, nombre, genero FROM productos LIMIT 5")
            productos = cursor.fetchall()
            for prod_id, nombre, genero in productos:
                print(f"   • {prod_id}: {nombre} ({genero})")
            if num_productos > 5:
                print(f"   ... y {num_productos - 5} más")
        
        # Verificar ventas
        cursor.execute("SELECT COUNT(*) FROM salidas")
        num_ventas = cursor.fetchone()[0]
        print(f"\n📊 VENTAS EN HISTORIAL: {num_ventas}")
        
        if num_ventas > 0:
            cursor.execute("""
                SELECT s.id_producto, s.cantidad_vendida, s.cliente, s.fecha_venta,
                       p.nombre as nombre_producto
                FROM salidas s
                LEFT JOIN productos p ON s.id_producto = p.id
                ORDER BY s.fecha_venta DESC
                LIMIT 5
            """)
            ventas = cursor.fetchall()
            for id_prod, cantidad, cliente, fecha, nombre_prod in ventas:
                estado = "✅ Activo" if nombre_prod else "❌ Eliminado"
                nombre = nombre_prod if nombre_prod else f"[{id_prod}]"
                print(f"   • {nombre}: {cantidad}ml - {cliente or 'N/A'} - {estado}")
        
        # Verificar constraint de foreign key
        cursor.execute("PRAGMA table_info(salidas)")
        columns_info = cursor.fetchall()
        
        cursor.execute("PRAGMA foreign_key_list(salidas)")
        foreign_keys = cursor.fetchall()
        
        print(f"\n🔗 FOREIGN KEYS EN SALIDAS: {len(foreign_keys)}")
        if foreign_keys:
            print("   ⚠️  Hay restricciones de integridad referencial")
        else:
            print("   ✅ Sin restricciones - historial independiente")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al verificar estado: {str(e)}")

if __name__ == "__main__":
    verificar_estado_bd()
