# -*- coding: utf-8 -*-
"""
Repositorio de PDFs - Capa de Acceso a Datos
Materiales Ibarra, S.A.
"""

import os
import shutil
from datetime import datetime
from typing import Optional
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class PDFRepository:
    """Repositorio para gestión de archivos PDF"""
    
    @staticmethod
    def save_pdf(pdf_data: bytes, filename: str, tipo: str = "cotizacion") -> Optional[str]:
        """Guarda un PDF en el storage"""
        try:
            fecha_actual = datetime.now().strftime("%Y%m%d")
            subcarpeta = f"{tipo}_{fecha_actual}"
            carpeta_destino = os.path.join(Config.FACTURAS_DIR, subcarpeta)
            
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino, exist_ok=True)
            
            ruta_completa = os.path.join(carpeta_destino, filename)
            
            with open(ruta_completa, "wb") as f:
                f.write(pdf_data)
            
            logger.info(f"PDF guardado: {ruta_completa}")
            return ruta_completa
            
        except Exception as e:
            logger.error(f"Error guardando PDF: {e}")
            return None
    
    @staticmethod
    def get_pdf(ruta_pdf: str) -> Optional[bytes]:
        """Lee un PDF desde el storage"""
        try:
            if os.path.exists(ruta_pdf):
                with open(ruta_pdf, "rb") as f:
                    return f.read()
            return None
        except Exception as e:
            logger.error(f"Error leyendo PDF: {e}")
            return None
    
    @staticmethod
    def delete_pdf(ruta_pdf: str) -> bool:
        """Elimina un PDF del storage"""
        try:
            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)
                logger.info(f"PDF eliminado: {ruta_pdf}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error eliminando PDF: {e}")
            return False
    
    @staticmethod
    def list_pdfs(tipo: str = None) -> list:
        """Lista todos los PDFs disponibles"""
        try:
            pdfs = []
            for root, dirs, files in os.walk(Config.FACTURAS_DIR):
                for file in files:
                    if file.endswith(".pdf"):
                        ruta_completa = os.path.join(root, file)
                        stat = os.stat(ruta_completa)
                        pdfs.append({
                            "nombre": file,
                            "ruta": ruta_completa,
                            "tamano": stat.st_size,
                            "fecha": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        })
            return pdfs
        except Exception as e:
            logger.error(f"Error listando PDFs: {e}")
            return []
    
    @staticmethod
    def create_backup(db_name: str) -> Optional[str]:
        """Crea un backup de la base de datos"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{db_name}_{timestamp}.bak"
            backup_path = os.path.join(Config.BACKUPS_DIR, backup_name)
            
            logger.info(f"Backup creado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creando backup: {e}")
            return None