import flet as ft
from typing import Optional
import time
import threading

class AlertManager:
    """Clase para manejar diferentes tipos de alertas y notificaciones"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        # Crear un contenedor para las alertas en la parte superior
        self.alert_container = ft.Container(
            content=ft.Column([]),
            padding=10,
            width=400,
            bgcolor=ft.Colors.TRANSPARENT,
        )
        
    def show_success(self, mensaje: str, duracion: int = 3000):
        """Muestra una alerta de éxito (verde)"""
        self._show_overlay_alert(mensaje, ft.Colors.GREEN_600, ft.Icons.CHECK_CIRCLE, duracion)
    
    def show_error(self, mensaje: str, duracion: int = 5000):
        """Muestra una alerta de error (rojo)"""
        self._show_overlay_alert(mensaje, ft.Colors.RED_600, ft.Icons.ERROR, duracion)
    
    def show_warning(self, mensaje: str, duracion: int = 4000):
        """Muestra una alerta de advertencia (naranja)"""
        self._show_overlay_alert(mensaje, ft.Colors.ORANGE_600, ft.Icons.WARNING, duracion)
    
    def show_info(self, mensaje: str, duracion: int = 3000):
        """Muestra una alerta informativa (azul)"""
        self._show_overlay_alert(mensaje, ft.Colors.BLUE_600, ft.Icons.INFO, duracion)
    
    def show_toast(self, mensaje: str, tipo: str = "info"):
        """Muestra un toast simple"""
        colores = {
            "success": ft.Colors.GREEN_600,
            "error": ft.Colors.RED_600,
            "warning": ft.Colors.ORANGE_600,
            "info": ft.Colors.BLUE_600
        }
        
        iconos = {
            "success": ft.Icons.CHECK,
            "error": ft.Icons.ERROR,
            "warning": ft.Icons.WARNING,
            "info": ft.Icons.INFO
        }
        
        self._show_overlay_alert(
            mensaje, 
            colores.get(tipo, ft.Colors.BLUE_600), 
            iconos.get(tipo, ft.Icons.INFO), 
            2000
        )
    
    def _show_overlay_alert(self, mensaje: str, color: str, icon: str, duracion: int):
        """Método interno para mostrar alertas usando overlay"""
        print(f"DEBUG: Intentando mostrar alerta: {mensaje}")
        try:
            # Variable para controlar la eliminación manual
            alert_removed = [False]  # Usar lista para modificar desde función anidada
            
            def close_alert(e):
                alert_removed[0] = True
                try:
                    if len(self.page.overlay) > 0:
                        # Buscar y eliminar esta alerta específica
                        for i, overlay_item in enumerate(self.page.overlay):
                            if hasattr(overlay_item, 'content') and overlay_item.content == alert_card:
                                alert_card.opacity = 0.0
                                self.page.update()
                                time.sleep(0.1)
                                self.page.overlay.pop(i)
                                self.page.update()
                                break
                except Exception as ex:
                    print(f"Error cerrando alerta manualmente: {ex}")
            
            # Crear la alerta como un cuadrito compacto con botón X
            alert_card = ft.Container(
                content=ft.Stack([
                    # Contenido principal
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(icon, color=ft.Colors.WHITE, size=24),
                            ft.Text(
                                mensaje, 
                                color=ft.Colors.WHITE, 
                                weight=ft.FontWeight.BOLD, 
                                size=12,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS
                            )
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8
                        ),
                        padding=ft.padding.only(top=20, bottom=15, left=15, right=15)
                    ),
                    # Botón X en la esquina superior derecha
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=16,
                            icon_color=ft.Colors.WHITE,
                            on_click=close_alert,
                            tooltip="Cerrar"
                        ),
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(top=2, right=2)
                    )
                ]),
                padding=0,
                bgcolor=color,
                border_radius=12,
                margin=ft.margin.only(bottom=10),
                animate_opacity=300,
                opacity=1.0,
                width=150,
                height=100,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(0, 4),
                )
            )
            
            # Añadir la alerta al overlay de la página
            overlay_container = ft.Container(
                content=alert_card,
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=50, right=20),
            )
            
            self.page.overlay.append(overlay_container)
            self.page.update()
            print(f"DEBUG: Alerta añadida al overlay")
            
            # Programar la eliminación automática de la alerta
            def remove_alert():
                time.sleep(duracion / 1000)  # Convertir ms a segundos
                # Solo eliminar si no fue cerrada manualmente
                if not alert_removed[0]:
                    try:
                        if len(self.page.overlay) > 0:
                            # Buscar y eliminar esta alerta específica
                            for i, overlay_item in enumerate(self.page.overlay):
                                if overlay_item == overlay_container:
                                    alert_card.opacity = 0.0
                                    self.page.update()
                                    time.sleep(0.3)
                                    self.page.overlay.pop(i)
                                    self.page.update()
                                    print(f"DEBUG: Alerta eliminada automáticamente del overlay")
                                    break
                    except Exception as e:
                        print(f"Error eliminando alerta automáticamente: {e}")
            
            # Ejecutar en un hilo separado para no bloquear la UI
            threading.Thread(target=remove_alert, daemon=True).start()
            
        except Exception as e:
            print(f"ERROR en _show_overlay_alert: {e}")
            print(f"Alerta: {mensaje}")
    
    def show_confirmation_dialog(self, titulo: str, mensaje: str, on_confirm, on_cancel=None):
        """Muestra un diálogo de confirmación usando overlay"""
        print(f"DEBUG: Creando diálogo de confirmación: {titulo}")
        
        def confirmar(e):
            print(f"DEBUG: Usuario confirmó la acción")
            self.close_overlay_dialog()
            if on_confirm:
                print(f"DEBUG: Ejecutando callback de confirmación")
                on_confirm()
            else:
                print(f"DEBUG: No hay callback de confirmación")
        
        def cancelar(e):
            print(f"DEBUG: Usuario canceló la acción")
            self.close_overlay_dialog()
            if on_cancel:
                on_cancel()
        
        # Crear el diálogo como overlay personalizado
        dialog_content = ft.Container(
            content=ft.Column([
                # Título
                ft.Row([
                    ft.Icon(ft.Icons.HELP, color=ft.Colors.ORANGE_600, size=24),
                    ft.Text(titulo, weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.ORANGE_600)
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(height=20),
                
                # Mensaje
                ft.Text(
                    mensaje, 
                    size=14, 
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.BLACK87
                ),
                
                ft.Divider(height=20),
                
                # Botones
                ft.Row([
                    ft.ElevatedButton(
                        "Cancelar",
                        on_click=cancelar,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREY_400,
                            color=ft.Colors.WHITE
                        ),
                        width=120
                    ),
                    ft.ElevatedButton(
                        "Confirmar",
                        on_click=confirmar,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_600,
                            color=ft.Colors.WHITE
                        ),
                        width=120
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            ], 
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            width=400,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 10),
            )
        )
        
        # Fondo semi-transparente que ocupa toda la ventana
        overlay_bg = ft.Container(
            content=dialog_content,
            bgcolor=ft.Colors.BLACK54,  # Fondo semi-transparente
            alignment=ft.alignment.center,
            expand=True,  # Ocupa todo el espacio disponible
        )
        
        # Guardar referencia para poder cerrar
        self.current_overlay_dialog = overlay_bg
        
        self.page.overlay.append(overlay_bg)
        self.page.update()
        print(f"DEBUG: Diálogo de confirmación mostrado en overlay")
    
    def close_overlay_dialog(self):
        """Cierra el diálogo de overlay actual"""
        if hasattr(self, 'current_overlay_dialog') and self.current_overlay_dialog:
            try:
                if self.current_overlay_dialog in self.page.overlay:
                    self.page.overlay.remove(self.current_overlay_dialog)
                    self.page.update()
                self.current_overlay_dialog = None
                print(f"DEBUG: Diálogo de overlay cerrado")
            except Exception as e:
                print(f"Error cerrando diálogo de overlay: {e}")
    
    def close_dialog(self):
        """Cierra el diálogo actual"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()