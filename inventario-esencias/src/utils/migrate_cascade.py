"""
Migración para cambiar la relación a eliminación en cascada
"""
import sqlite3
import os

def migrate_cascade_delete():
    """Modifica la tabla para permitir eliminación en cascada"""
    
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
        
        print("🔄 Iniciando migración para eliminación en cascada...")
        
        # Deshabilitar foreign keys temporalmente
        cursor.execute("PRAGMA foreign_keys=OFF")
        
        # Crear nueva tabla de salidas con ON DELETE CASCADE
        cursor.execute("""
            CREATE TABLE salidas_new (
                id TEXT PRIMARY KEY,
                id_producto TEXT NOT NULL,
                cantidad_vendida REAL NOT NULL,
                precio_venta REAL NOT NULL,
                fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
                cliente TEXT,
                ganancia REAL DEFAULT 0.0,
                FOREIGN KEY (id_producto) REFERENCES productos (id) ON DELETE CASCADE
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
        print("✅ Migración completada: Ahora se eliminarán las ventas automáticamente")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = migrate_cascade_delete()
    if success:
        print("🎉 Migración de cascada completada exitosamente")
    else:
        print("💥 Error en la migración de cascada")
