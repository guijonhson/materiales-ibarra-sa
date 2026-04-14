# -*- coding: utf-8 -*-
"""
Archivo de inicio para Materiales Ibarra, S.A.
Ejecutar con doble clic - Inicia la aplicación directamente
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ejecutar la aplicación principal
from ui.app_ui import main

if __name__ == "__main__":
    main()