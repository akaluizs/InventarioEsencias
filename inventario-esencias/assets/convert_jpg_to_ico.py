"""
Script para convertir icono.jpg a icono.ico
Esto ayuda porque los archivos ICO funcionan mejor como iconos de ventana
"""

import os
import sys

# Verificar si existe el JPG
jpg_path = "icono.jpg"
if not os.path.exists(jpg_path):
    print(f"❌ No se encontró {jpg_path}")
    print(f"📁 Buscando en directorio actual: {os.getcwd()}")
    print("📋 Archivos disponibles:")
    for file in os.listdir("."):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.ico')):
            print(f"   - {file}")
    sys.exit(1)

try:
    from PIL import Image
    print(f"✅ Pillow disponible, convirtiendo {jpg_path} a ICO...")
    
    # Abrir y redimensionar la imagen
    with Image.open(jpg_path) as img:
        # Convertir a RGBA si es necesario
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Redimensionar a tamaños estándar de icono
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Guardar como ICO
        ico_path = "icono.ico"
        images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes])
        
        print(f"✅ Icono ICO creado: {ico_path}")
        print(f"📏 Tamaños incluidos: {sizes}")
        
        # Verificar el resultado
        if os.path.exists(ico_path):
            size_mb = os.path.getsize(ico_path) / 1024
            print(f"📁 Tamaño archivo: {size_mb:.1f} KB")
        
except ImportError:
    print("❌ Pillow no está instalado")
    print("📦 Ejecuta: pip install pillow")
    print("🔄 O usa online converter: https://convertio.co/jpg-ico/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Verifica que el archivo JPG sea válido")
