"""
Script de migración para agregar la columna género a la tabla productos
"""
import sqlite3
import os

def migrate_add_genero_column():
    """Agrega la columna genero a la tabla productos si no existe"""
    
    # Buscar la base de datos en el directorio actual y en el directorio padre
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
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(productos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'genero' in columns:
            print("La columna 'genero' ya existe en la tabla productos")
            conn.close()
            return True
        
        print("Agregando columna 'genero' a la tabla productos...")
        
        # Agregar la columna genero con valor por defecto 'Unisex'
        cursor.execute("ALTER TABLE productos ADD COLUMN genero TEXT DEFAULT 'Unisex'")
        
        # Actualizar todos los registros existentes para que tengan 'Unisex' como género
        cursor.execute("UPDATE productos SET genero = 'Unisex' WHERE genero IS NULL")
        
        # Confirmar los cambios
        conn.commit()
        
        print("✅ Migración completada exitosamente")
        print("Todos los productos existentes ahora tienen género 'Unisex'")
        
        # Verificar que la columna se agregó correctamente
        cursor.execute("PRAGMA table_info(productos)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Columnas actuales en productos: {columns}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🔄 Iniciando migración de base de datos...")
    success = migrate_add_genero_column()
    if success:
        print("🎉 Migración completada exitosamente")
    else:
        print("💥 Error en la migración")
