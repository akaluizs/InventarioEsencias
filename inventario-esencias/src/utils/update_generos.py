"""
Script para actualizar los productos existentes con géneros apropiados
"""
import sqlite3
import os

def actualizar_generos_productos():
    """Actualiza los géneros de productos existentes basándose en sus nombres"""
    
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
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todos los productos actuales
        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
        
        print(f"Encontrados {len(productos)} productos para actualizar...")
        
        # Mapeo de géneros basado en nombres típicos de esencias
        generos_map = {
            'lavanda': 'Unisex',
            'rosa': 'Femenino', 
            'eucalipto': 'Masculino',
            'ylang': 'Femenino',
            'davo': 'Masculino',
            'saber': 'Masculino',
            'vainilla': 'Femenino',
            'menta': 'Unisex',
            'jazmín': 'Femenino',
            'sándalo': 'Masculino',
            'bergamota': 'Unisex',
            'citrico': 'Unisex',
            'limón': 'Unisex',
            'naranja': 'Unisex'
        }
        
        # Actualizar cada producto
        for producto_id, nombre in productos:
            genero = 'Unisex'  # Por defecto
            
            # Buscar coincidencias en el nombre
            nombre_lower = nombre.lower()
            for clave, genero_asignado in generos_map.items():
                if clave in nombre_lower:
                    genero = genero_asignado
                    break
            
            # Actualizar el producto
            cursor.execute(
                "UPDATE productos SET genero = ? WHERE id = ?",
                (genero, producto_id)
            )
            
            print(f"  • {nombre} ({producto_id}) → {genero}")
        
        # Confirmar los cambios
        conn.commit()
        
        print("✅ Géneros actualizados exitosamente")
        
        # Verificar resultados
        cursor.execute("SELECT genero, COUNT(*) FROM productos GROUP BY genero")
        resultados = cursor.fetchall()
        
        print("\nDistribución por género:")
        for genero, cantidad in resultados:
            print(f"  • {genero}: {cantidad} productos")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🔄 Actualizando géneros de productos existentes...")
    success = actualizar_generos_productos()
    if success:
        print("🎉 Actualización completada exitosamente")
    else:
        print("💥 Error en la actualización")
