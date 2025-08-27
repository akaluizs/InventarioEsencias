"""
Migración para agregar tabla de frascos y tipo de producto
"""
import sqlite3
import os

def migrate_add_frascos():
    """Agrega la tabla frascos y el campo tipo_producto"""
    
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
        
        print("🔄 Iniciando migración para frascos...")
        
        # Verificar si la tabla frascos ya existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='frascos'")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            print("📦 Creando tabla de frascos...")
            cursor.execute("""
                CREATE TABLE frascos (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    costo REAL NOT NULL,
                    capacidad_ml REAL NOT NULL,
                    stock_actual INTEGER DEFAULT 0
                )
            """)
            print("✅ Tabla 'frascos' creada")
        else:
            print("✅ Tabla 'frascos' ya existe")
        
        # Verificar si la columna tipo_producto ya existe en productos
        cursor.execute("PRAGMA table_info(productos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'tipo_producto' not in columns:
            print("🏷️ Agregando campo tipo_producto...")
            cursor.execute("ALTER TABLE productos ADD COLUMN tipo_producto TEXT DEFAULT 'esencia'")
            
            # Actualizar todos los productos existentes como 'esencia'
            cursor.execute("UPDATE productos SET tipo_producto = 'esencia' WHERE tipo_producto IS NULL")
            print("✅ Campo 'tipo_producto' agregado")
        else:
            print("✅ Campo 'tipo_producto' ya existe")
        
        conn.commit()
        print("🎉 Migración completada exitosamente")
        print("Ahora puedes manejar tanto esencias como frascos")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = migrate_add_frascos()
    if success:
        print("🎉 Sistema actualizado: Esencias + Frascos disponibles")
    else:
        print("💥 Error en la migración")
