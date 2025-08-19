"""
Script para generar un icono .ico para la aplicación de Inventario de Esencias
Requiere: pip install pillow

Ejecutar: python generate_icon.py
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_app_icon():
        """Crear un icono de aplicación estilo esencias/laboratorio"""
        # Crear imagen de 256x256 para mejor calidad
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Fondo circular con gradiente verde
        center = size // 2
        radius = center - 10
        
        # Dibujar círculo de fondo
        draw.ellipse([10, 10, size-10, size-10], 
                    fill=(46, 125, 50, 255), 
                    outline=(27, 94, 32, 255), width=6)
        
        # Frasco principal (cuerpo)
        frasco_x = center - 30
        frasco_y = center - 40
        frasco_width = 60
        frasco_height = 80
        
        # Cuerpo del frasco
        draw.rounded_rectangle([frasco_x, frasco_y, frasco_x + frasco_width, frasco_y + frasco_height], 
                              radius=8, fill=(240, 248, 255, 255), 
                              outline=(76, 175, 80, 255), width=4)
        
        # Cuello del frasco
        cuello_x = center - 15
        cuello_width = 30
        cuello_height = 15
        draw.rectangle([cuello_x, frasco_y - cuello_height, cuello_x + cuello_width, frasco_y], 
                      fill=(240, 248, 255, 255), outline=(76, 175, 80, 255))
        
        # Tapa del frasco
        tapa_x = center - 18
        tapa_width = 36
        tapa_height = 8
        draw.rounded_rectangle([tapa_x, frasco_y - cuello_height - tapa_height, 
                               tapa_x + tapa_width, frasco_y - cuello_height], 
                              radius=4, fill=(139, 195, 74, 255))
        
        # Líquido interior (verde claro)
        liquido_margin = 8
        liquido_height = 50
        draw.rounded_rectangle([frasco_x + liquido_margin, frasco_y + frasco_height - liquido_height, 
                               frasco_x + frasco_width - liquido_margin, frasco_y + frasco_height - liquido_margin], 
                              radius=4, fill=(129, 199, 132, 200))
        
        # Etiqueta blanca
        etiqueta_height = 25
        etiqueta_y = center - 5
        draw.rounded_rectangle([frasco_x + 8, etiqueta_y, frasco_x + frasco_width - 8, etiqueta_y + etiqueta_height], 
                              radius=3, fill=(255, 255, 255, 230), outline=(200, 200, 200, 100))
        
        # Burbujas decorativas
        bubble_positions = [(center - 50, center - 60, 8), (center + 40, center - 50, 6), 
                           (center - 45, center + 20, 5), (center + 35, center + 15, 4)]
        
        for x, y, r in bubble_positions:
            draw.ellipse([x-r, y-r, x+r, y+r], fill=(129, 199, 132, 150))
        
        # Guardar como PNG primero
        png_path = "app_icon.png"
        img.save(png_path, "PNG")
        print(f"✅ Icono PNG creado: {png_path}")
        
        # Crear versiones en diferentes tamaños para ICO
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for icon_size in sizes:
            resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Guardar como ICO
        ico_path = "app_icon.ico"
        images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes])
        print(f"✅ Icono ICO creado: {ico_path}")
        
        return png_path, ico_path
    
    if __name__ == "__main__":
        print("🎨 Generando icono de aplicación...")
        png_file, ico_file = create_app_icon()
        print(f"\n🎯 Iconos generados exitosamente:")
        print(f"   📁 PNG: {png_file}")
        print(f"   📁 ICO: {ico_file}")
        print(f"\n💡 Para usar en Flet:")
        print(f"   page.window_icon = '{ico_file}'")

except ImportError:
    print("❌ Error: Pillow no está instalado")
    print("📦 Instalar con: pip install pillow")
except Exception as e:
    print(f"❌ Error generando icono: {e}")
