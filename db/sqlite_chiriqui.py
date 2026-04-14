# -*- coding: utf-8 -*-
"""
Base de Datos SQLite - Sucursal Chiriquí
Materiales Ibarra, S.A.
"""

import sqlite3
import os
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class ChiriquiDB:
    _instance = None
    _connection = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def connect(cls):
        try:
            db_path = Config.SQLITE_CHIRIQUI
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            cls._connection = sqlite3.connect(db_path, check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row
            cls._create_tables()
            logger.info("✓ Conexión a SQLite Chiriquí establecida")
            return cls._connection
        except Exception as e:
            logger.error(f"✗ Error al conectar a SQLite Chiriquí: {e}")
            return None
    
    @classmethod
    def _create_tables(cls):
        cursor = cls._connection.cursor()
        
        # Tabla de materiales (Error Medio L38-90: Agregar índices)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materiales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mongo_id TEXT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                categoria TEXT,
                unidad TEXT,
                activo INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Error Medio L38-90: Crear índices para búsquedas frecuentes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_materiales_nombre ON materiales(nombre)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_materiales_categoria ON materiales(categoria)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_materiales_mongo_id ON materiales(mongo_id)")
        
        # Tabla de cotizaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mongo_id TEXT,
                cliente_nombre TEXT NOT NULL,
                cliente_cedula TEXT,
                materiales TEXT NOT NULL,
                total REAL NOT NULL,
                sucursal TEXT DEFAULT 'CHIRIQUI',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pdf_path TEXT,
                estado TEXT DEFAULT 'PENDIENTE'
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cotizaciones_cliente ON cotizaciones(cliente_nombre)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cotizaciones_mongo_id ON cotizaciones(mongo_id)")
        
        # Tabla de facturas fiscales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mongo_id TEXT,
                numero_factura TEXT UNIQUE NOT NULL,
                cedula_cliente TEXT NOT NULL,
                cliente_nombre TEXT NOT NULL,
                subtotal REAL NOT NULL,
                itbms REAL NOT NULL,
                total REAL NOT NULL,
                sucursal TEXT DEFAULT 'CHIRIQUI',
                xml_dgi TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_numero ON facturas(numero_factura)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_facturas_mongo_id ON facturas(mongo_id)")
        
        cls._connection.commit()
        logger.info("✓ Tablas creadas en Chiriquí")
    
    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls.connect()
        return cls._connection
    
    @classmethod
    def close(cls):
        if cls._connection:
            cls._connection.close()

def get_chiriqui_db():
    return ChiriquiDB.get_connection()