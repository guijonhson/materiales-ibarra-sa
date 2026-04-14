# -*- coding: utf-8 -*-
"""
Configuración Principal de la Aplicación
Materiales Ibarra, S.A. - Sistema de Gestión

IMPORTANTE: Este archivo debe funcionar en:
- Windows (desarrollo y ejecutable)
- Linux (futuro)
- detection automática de la ruta del proyecto
"""

import os
import sys

def _get_base_dir():
    """Obtiene el directorio base de la aplicación de forma dinámica"""
    # Si está congelado (PyInstaller), usar directorio del exe
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    
    # Detectar la ruta del proyecto automáticamente
    # Ir desde config/ hacia arriba (project root)
    config_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(config_dir)
    
    # Verificar que estamos en la raíz del proyecto
    # Buscar archivo indicador (iniciar.pyw o requirements.txt)
    if not os.path.exists(os.path.join(base_dir, 'iniciar.pyw')):
        # Si no encuentra, intentar desde el directorio actual de trabajo
        base_dir = os.getcwd()
    
    return base_dir

# Obtener BASE_DIR dinámicamente
BASE_DIR = _get_base_dir()

# Detectar sistema operativo
ES_WINDOWS = sys.platform == 'win32'
ES_LINUX = sys.platform.startswith('linux')

class Config:
    """Configuración centralizada del sistema"""
    
    # ============================================================
    # MONGODB - SIEMPRE LOCAL (Principal)
    # ============================================================
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = "materiales_ibarra"
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
    
    # ============================================================
    # SQLITE - Rutas basadas en BASE_DIR (réplicas locales)
    # ============================================================
    # Usar BASE_DIR para que funcione en cualquier ubicación
    _DB_FOLDER = "db"
    
    SQLITE_CHIRIQUI = os.path.join(BASE_DIR, _DB_FOLDER, "chiriqui.db")
    SQLITE_VERAGUAS = os.path.join(BASE_DIR, _DB_FOLDER, "veraguas.db")
    SQLITE_CHITRE = os.path.join(BASE_DIR, _DB_FOLDER, "chitre.db")
    
    # ============================================================
    # CARPETAS DE STORAGE Y LOGS
    # ============================================================
    STORAGE_DIR = os.path.join(BASE_DIR, "storage")
    FACTURAS_DIR = os.path.join(STORAGE_DIR, "facturas")
    BACKUPS_DIR = os.path.join(STORAGE_DIR, "backups")
    DB_DIR = os.path.join(BASE_DIR, _DB_FOLDER)
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    
    # ============================================================
    # CREAR DIRECTORIOS SI NO EXISTEN
    # ============================================================
    _DIRECTORIES = [
        STORAGE_DIR,
        FACTURAS_DIR,
        BACKUPS_DIR,
        DB_DIR,
        LOGS_DIR
    ]
    
    @classmethod
    def ensure_directories(cls):
        """Crea todos los directorios necesarios"""
        for directory in cls._DIRECTORIES:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception as e:
                    print(f"Advertencia: No se pudo crear {directory}: {e}")
    
        # ============================================================
    # CONFIGURACIÓN DE FACTURACIÓN (DGI)
    # ============================================================
    DGI_TIPO_DOCUMENTO = "FACTURA"
    DGI_TIPO_EMISION = "01"
    DGI_ESTADO = "ACTIVO"
    
    # ============================================================
    # CONFIGURACIÓN DEL CHATBOT
    # ============================================================
    CHATBOT_ENABLED = True
    CHATBOT_NAME = "Asistente Materiales Ibarra"
    
    # ============================================================
    # REPLICACIÓN
    # ============================================================
    REPLICACION_INTERVAL = 5  # segundos
    REPLICACION_HABILITADA = True
    
    # ============================================================
    # FORMATOS
    # ============================================================
    DECIMAL_PRECISION = 2
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class Sucursales:
    """Configuración de sucursales"""
    CHIRIQUI = {
        "nombre": "Mat. Ibarra - Chiriquí",
        "ubicacion": "Vía Panamericana, Chiriquí",
        "db": Config.SQLITE_CHIRIQUI,
        "codigo": "CH"
    }
    VERAGUAS = {
        "nombre": "Mat. Ibarra - Veraguas",
        "ubicacion": "Vía Panamericana frente al Mall de Santiago",
        "db": Config.SQLITE_VERAGUAS,
        "codigo": "VR"
    }
    CHITRE = {
        "nombre": "Mat. Ibarra - Chitré",
        "ubicacion": "Frente a la plaza del Hotel Gran Azuero",
        "db": Config.SQLITE_CHITRE,
        "codigo": "CT"
    }


# ============================================================
# VARIABLES EXPORTABLES PARA USO EXTERNO
# ============================================================
__all__ = [
    'BASE_DIR',
    'ES_WINDOWS',
    'ES_LINUX',
    'Config',
    'Sucursales'
]

# Crear directorios al cargar el módulo
Config.ensure_directories()


# ============================================================
# DEBUG: Imprimir configuración al importar
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("CONFIGURACIÓN - Materiales Ibarra, S.A.")
    print("=" * 50)
    print(f"Sistema: {'Windows' if ES_WINDOWS else 'Linux'}")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"MongoDB: {Config.MONGO_URI}")
    print(f"Chiriquí DB: {Config.SQLITE_CHIRIQUI}")
    print(f"Veraguas DB: {Config.SQLITE_VERAGUAS}")
    print(f"Chitré DB: {Config.SQLITE_CHITRE}")
    print(f"Facturas: {Config.FACTURAS_DIR}")
    print("=" * 50)