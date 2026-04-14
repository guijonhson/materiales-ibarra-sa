# -*- coding: utf-8 -*-
"""
Conexión a MongoDB - Base de Datos Principal
Materiales Ibarra, S.A.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, NetworkTimeout
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None
    _connected = False
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def connect(cls):
        try:
            # Error Crítico L28: Agregar reintentos y pool de conexiones
            cls._client = MongoClient(
                Config.MONGO_URI, 
                serverSelectionTimeoutMS=5000, 
                maxPoolSize=10, 
                retryWrites=True, 
                retryReads=True,
                connectTimeoutMS=10000,
                socketTimeoutMS=30000
            )
            cls._db = cls._client[Config.MONGO_DB]
            cls._client.admin.command('ping')
            cls._connected = True
            logger.info("✓ Conexión a MongoDB establecida correctamente")
            cls._create_collections()
            return cls._db
        except ConnectionFailure as e:
            logger.error(f"✗ Error de conexión a MongoDB (auth/network): {e}")
            cls._connected = False
            return None
        except NetworkTimeout as e:
            logger.error(f"✗ Timeout de red MongoDB: {e}")
            cls._connected = False
            return None
        except OperationFailure as e:
            logger.error(f"✗ Error de operación MongoDB: {e}")
            cls._connected = False
            return None
        except Exception as e:
            logger.error(f"✗ Error al conectar a MongoDB: {e}")
            cls._connected = False
            return None
    
    @classmethod
    def _create_collections(cls):
        """Crea las colecciones si no existen"""
        try:
            db = cls._db
            existing_collections = db.list_collection_names()
            
            required_collections = ["materiales", "cotizaciones", "facturas"]
            
            for coll_name in required_collections:
                if coll_name not in existing_collections:
                    db.create_collection(coll_name)
                    logger.info(f"✓ Colección '{coll_name}' creada en MongoDB")
                
                # Error Alto L47-63: Verificar si índices existen antes de crear
                # Error Medio L34-38: Verificar tipos de índices correctamente
                index_info = db[coll_name].index_information()
                
                if coll_name == "materiales":
                    if "nombre_1" not in index_info:
                        db[coll_name].create_index("nombre")
                        logger.info("✓ Índice 'nombre' creado en materiales")
                    if "categoria_1" not in index_info:
                        db[coll_name].create_index("categoria")
                        logger.info("✓ Índice 'categoria' creado en materiales")
                        
                elif coll_name == "cotizaciones":
                    if "cliente_nombre_1" not in index_info:
                        db[coll_name].create_index("cliente_nombre")
                        logger.info("✓ Índice 'cliente_nombre' creado en cotizaciones")
                    if "sucursal_1" not in index_info:
                        db[coll_name].create_index("sucursal")
                        logger.info("✓ Índice 'sucursal' creado en cotizaciones")
                        
                elif coll_name == "facturas":
                    if "numero_factura_1" not in index_info:
                        db[coll_name].create_index("numero_factura", unique=True)
                        logger.info("✓ Índice único 'numero_factura' creado en facturas")
                    if "cedula_cliente_1" not in index_info:
                        db[coll_name].create_index("cedula_cliente")
                        logger.info("✓ Índice 'cedula_cliente' creado en facturas")
                        
            logger.info("✓ Colecciones inicializadas en MongoDB")
        except Exception as e:
            logger.error(f"✗ Error creando colecciones: {e}")
    
    @classmethod
    def is_connected(cls):
        return cls._connected and cls._db is not None
    
    @classmethod
    def get_database(cls):
        if cls._db is None:
            cls.connect()
        return cls._db
    
    @classmethod
    def get_collection(cls, name):
        connected = cls.is_connected()
        logger.info(f"DEBUG get_collection: name={name}, is_connected={connected}, _db={cls._db is not None}, _connected={cls._connected}")
        if connected:
            return cls._db[name]
        # Error Alto L80-83: Agregar logging cuando retorna None
        logger.warning(f"Conexión a MongoDB perdida, colección '{name}' no disponible")
        return None
    
    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            logger.info("Conexión a MongoDB cerrada")

def get_mongo_db():
    return MongoDBConnection.get_database()

def get_collection(nombre_coleccion):
    return MongoDBConnection.get_collection(nombre_coleccion)