# -*- coding: utf-8 -*-
"""
Gestor de Conexiones - Manejo de Todas las Bases de Datos
Materiales Ibarra, S.A.
"""

from db.mongo import MongoDBConnection
from db.sqlite_chiriqui import ChiriquiDB
from db.sqlite_veraguas import VeraguasDB
from db.sqlite_chitre import ChitréDB
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Gestor centralizado de todas las conexiones de base de datos"""
    
    def __init__(self):
        self.mongo_connected = False
        self.chiriqui_connected = False
        self.veraguas_connected = False
        self.chitre_connected = False
    
    def initialize_all(self):
        """Inicializa todas las conexiones de base de datos"""
        try:
            # Conectar a MongoDB
            db = MongoDBConnection.connect()
            if db is not None:
                self.mongo_connected = True
                logger.info("✓ MongoDB conectado")
            else:
                logger.warning("⚠ MongoDB no disponible, usando SQLite local")
        except Exception as e:
            logger.error(f"✗ Error inicializando MongoDB: {e}")
        
        try:
            # Conectar a SQLite Chiriquí
            if ChiriquiDB.connect():
                self.chiriqui_connected = True
                logger.info("✓ SQLite Chiriquí conectado")
        except Exception as e:
            logger.error(f"✗ Error inicializando Chiriquí: {e}")
        
        try:
            # Conectar a SQLite Veraguas
            if VeraguasDB.connect():
                self.veraguas_connected = True
                logger.info("✓ SQLite Veraguas conectado")
        except Exception as e:
            logger.error(f"✗ Error inicializando Veraguas: {e}")
        
        try:
            # Conectar a SQLite Chitré
            if ChitréDB.connect():
                self.chitre_connected = True
                logger.info("✓ SQLite Chitré conectado")
        except Exception as e:
            logger.error(f"✗ Error inicializando Chitré: {e}")
    
    def get_status(self):
        """Retorna el estado de las conexiones"""
        return {
            "mongodb": self.mongo_connected,
            "chiriqui": self.chiriqui_connected,
            "veraguas": self.veraguas_connected,
            "chitre": self.chitre_connected
        }
    
    def close_all(self):
        """Cierra todas las conexiones"""
        MongoDBConnection.close()
        ChiriquiDB.close()
        VeraguasDB.close()
        ChitréDB.close()
        logger.info("✓ Todas las conexiones cerradas")

# Instancia global del gestor de conexiones
connection_manager = ConnectionManager()