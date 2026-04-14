# -*- coding: utf-8 -*-
"""
Punto de Entrada Principal - Materiales Ibarra, S.A.
Sistema de Gestión Integral
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app_ui import main

if __name__ == "__main__":
    main()