"""
Migración para agregar soft delete (eliminación lógica)
"""
import sqlite3
import os

def migrate_soft_delete():
    """Agrega campo 'activo' para eliminación lógica"""
    
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
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(productos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'activo' in columns:
            print("La columna 'activo' ya existe en la tabla productos")
            conn.close()
            return True
        
        print("🔄 Agregando columna 'activo' para soft delete...")
        
        # Agregar la columna activo con valor por defecto True (1)
        cursor.execute("ALTER TABLE productos ADD COLUMN activo INTEGER DEFAULT 1")
        
        # Asegurar que todos los productos existentes estén activos
        cursor.execute("UPDATE productos SET activo = 1 WHERE activo IS NULL")
        
        conn.commit()
        print("✅ Migración completada: Ahora se puede usar eliminación lógica")
        print("Los productos se marcarán como inactivos en lugar de eliminarse")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    success = migrate_soft_delete()
    if success:
        print("🎉 Migración de soft delete completada exitosamente")
    else:
        print("💥 Error en la migración de soft delete")
