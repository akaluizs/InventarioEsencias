"""
Revertir migración de cascada - mantener historial independiente
"""
import sqlite3
import os

def revert_cascade_delete():
    """Revierte la eliminación en cascada y mantiene el historial independiente"""
    
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
        return False
    
    print(f"Usando base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Revirtiendo eliminación en cascada...")
        print("📋 El historial se mantendrá independiente del inventario")
        
        # Deshabilitar foreign keys temporalmente
        cursor.execute("PRAGMA foreign_keys=OFF")
        
        # Crear nueva tabla de salidas SIN CASCADE (historial independiente)
        cursor.execute("""
            CREATE TABLE salidas_new (
                id TEXT PRIMARY KEY,
                id_producto TEXT NOT NULL,
                cantidad_vendida REAL NOT NULL,
                precio_venta REAL NOT NULL,
                fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
                cliente TEXT,
                ganancia REAL DEFAULT 0.0
            )
        """)
        
        # Copiar datos de la tabla antigua a la nueva
        cursor.execute("""
            INSERT INTO salidas_new 
            SELECT * FROM salidas
        """)
        
        # Eliminar tabla antigua
        cursor.execute("DROP TABLE salidas")
        
        # Renombrar nueva tabla
        cursor.execute("ALTER TABLE salidas_new RENAME TO salidas")
        
        # Rehabilitar foreign keys
        cursor.execute("PRAGMA foreign_keys=ON")
        
        conn.commit()
        print("✅ Reversión completada:")
        print("   - Los productos se pueden eliminar del inventario")
        print("   - El historial de ventas se mantiene para auditoría")
        print("   - No hay dependencias entre inventario e historial")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la reversión: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = revert_cascade_delete()
    if success:
        print("🎉 Reversión completada: Historial independiente del inventario")
    else:
        print("💥 Error en la reversión")
