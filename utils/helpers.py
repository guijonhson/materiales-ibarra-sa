# -*- coding: utf-8 -*-
"""
Helpers - Funciones Auxiliares
Materiales Ibarra, S.A.
"""

import os
import sys
from datetime import datetime

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_timestamp() -> str:
    """Retorna la fecha y hora actual"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def pause():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")

def print_header(title: str):
    """Imprime un encabezado formateado"""
    width = 60
    print("=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_menu(options: list):
    """Imprime un menú de opciones"""
    print()
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print()

def get_option(max_option: int) -> int:
    """Solicita una opción al usuario"""
    try:
        option = int(input("  Opción: "))
        if 1 <= option <= max_option:
            return option
    except ValueError:
        pass
    return 0

def confirm(message: str) -> bool:
    """Solicita confirmación al usuario"""
    response = input(f"{message} (S/N): ").upper().strip()
    return response == 'S'

def sanitize_input(text: str) -> str:
    """Sanitiza la entrada del usuario"""
    if text is None:
        return ""
    return text.strip()

def get_app_path() -> str:
    """Retorna la ruta del directorio de la aplicación"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))