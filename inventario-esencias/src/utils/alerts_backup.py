import flet as ft
from typing import Optional

class AlertManager:
    """Clase para manejar diferentes tipos de alertas y notificaciones"""
    
    def __init__(self, page: ft.Page):
        self.page = page
    
    def show_success(self, mensaje: str, duracion: int = 3000):
        """Muestra una alerta de éxito (verde)"""
        snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ]),
            bgcolor=ft.Colors.GREEN_600,
            action="OK",
            action_color=ft.Colors.WHITE,
            duration=duracion,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
    
    def show_error(self, mensaje: str, duracion: int = 5000):
        """Muestra una alerta de error (rojo)"""
        snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE),
                ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ]),
            bgcolor=ft.Colors.RED_600,
            action="OK",
            action_color=ft.Colors.WHITE,
            duration=duracion,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
    
    def show_warning(self, mensaje: str, duracion: int = 4000):
        """Muestra una alerta de advertencia (naranja)"""
        snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.WHITE),
                ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ]),
            bgcolor=ft.Colors.ORANGE_600,
            action="OK",
            action_color=ft.Colors.WHITE,
            duration=duracion,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
    
    def show_info(self, mensaje: str, duracion: int = 3000):
        """Muestra una alerta informativa (azul)"""
        snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE),
                ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ]),
            bgcolor=ft.Colors.BLUE_600,
            action="OK",
            action_color=ft.Colors.WHITE,
            duration=duracion,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
    
    def show_confirmation_dialog(self, titulo: str, mensaje: str, on_confirm, on_cancel=None):
        """Muestra un diálogo de confirmación"""
        def confirmar(e):
            dialog.open = False
            self.page.update()
            if on_confirm:
                on_confirm()
        
        def cancelar(e):
            dialog.open = False
            self.page.update()
            if on_cancel:
                on_cancel()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.HELP, color=ft.Colors.ORANGE_600),
                ft.Text(titulo, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton(
                    "Confirmar", 
                    on_click=confirmar,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_custom_dialog(self, titulo: str, contenido, acciones=None):
        """Muestra un diálogo personalizado"""
        if acciones is None:
            acciones = [
                ft.TextButton(
                    "OK", 
                    on_click=lambda e: self.close_dialog()
                )
            ]
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
            content=contenido,
            actions=acciones,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def close_dialog(self):
        """Cierra el diálogo actual"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def show_toast(self, mensaje: str, tipo: str = "info"):
        """Muestra un toast simple (usando SnackBar simplificado)"""
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
        
        snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(iconos.get(tipo, ft.Icons.INFO), color=ft.Colors.WHITE, size=20),
                ft.Text(mensaje, color=ft.Colors.WHITE)
            ], tight=True),
            bgcolor=colores.get(tipo, ft.Colors.BLUE_600),
            duration=2000,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(5),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=5),
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
    
    def show_progress_dialog(self, titulo: str, mensaje: str):
        """Muestra un diálogo con barra de progreso"""
        progress_ring = ft.ProgressRing()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text(mensaje),
                ft.Container(
                    content=progress_ring,
                    alignment=ft.alignment.center,
                    padding=20
                )
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
        return dialog  # Retorna el diálogo para poder cerrarlo después
