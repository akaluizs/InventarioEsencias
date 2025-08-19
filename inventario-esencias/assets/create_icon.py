# Para crear un icono PNG con Python (se ejecutaría por separado)
from PIL import Image, ImageDraw
import os

def create_app_icon():
    # Crear una imagen de 64x64 píxeles
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fondo circular verde
    draw.ellipse([4, 4, size-4, size-4], fill=(46, 125, 50, 255), outline=(27, 94, 32, 255), width=2)
    
    # Frasco principal (rectángulo redondeado)
    draw.rounded_rectangle([24, 20, 40, 48], radius=2, fill=(232, 245, 232, 255), outline=(76, 175, 80, 255), width=2)
    
    # Cuello del frasco
    draw.rectangle([28, 16, 36, 20], fill=(232, 245, 232, 255), outline=(76, 175, 80, 255))
    
    # Tapa
    draw.rounded_rectangle([27, 14, 37, 16], radius=1, fill=(139, 195, 74, 255))
    
    # Líquido interior
    draw.rounded_rectangle([26, 24, 38, 46], radius=1, fill=(129, 199, 132, 200))
    
    # Etiqueta
    draw.rounded_rectangle([26, 28, 38, 36], radius=1, fill=(255, 255, 255, 230))
    
    return img

# No ejecutar automáticamente, solo crear el script
print("Script de generación de icono creado. Ejecutar por separado si se necesita generar el PNG.")
