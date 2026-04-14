# -*- coding: utf-8 -*-
"""
Repositorio de Cotizaciones - Capa de Acceso a Datos
Materiales Ibarra, S.A.
"""

from typing import List, Optional
from models.cotizacion import Cotizacion, ItemCotizacion
from db.mongo import get_collection
from db.sqlite_chiriqui import get_chiriqui_db
from db.sqlite_veraguas import get_veraguas_db
import json
import logging

logger = logging.getLogger(__name__)

class CotizacionRepository:
    """Repositorio para gestión de cotizaciones"""
    
    @staticmethod
    def create(cotizacion: Cotizacion) -> Optional[str]:
        """Crea una nueva cotización"""
        mongo_id = None
        try:
            cotizacion.calcular_total()
            
            # Guardar en MongoDB
            collection = get_collection("cotizaciones")
            if collection is not None:
                data = cotizacion.to_dict()
                data["items"] = [item.to_dict() for item in cotizacion.items]
                result = collection.insert_one(data)
                mongo_id = str(result.inserted_id)
                logger.info(f"Cotización guardada en MongoDB: {mongo_id}")
            
            # Replicar en SQLite
            conn = get_chiriqui_db()
            if conn is not None:
                cursor = conn.cursor()
                items_json = json.dumps([item.to_dict() for item in cotizacion.items], ensure_ascii=False)
                cursor.execute("""
                    INSERT INTO cotizaciones (cliente_nombre, cliente_cedula, materiales, total, sucursal, estado)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (cotizacion.cliente_nombre, cotizacion.cliente_cedula, 
                      items_json, cotizacion.total, cotizacion.sucursal, cotizacion.estado))
                conn.commit()
                sqlite_id = cursor.lastrowid
                
            return mongo_id
                
        except Exception as e:
            logger.error(f"Error creando cotización: {e}")
            return mongo_id
    
    @staticmethod
    def get_all() -> List[Cotizacion]:
        """Obtiene todas las cotizaciones"""
        cotizaciones = []
        
        try:
            collection = get_collection("cotizaciones")
            if collection is not None:
                for doc in collection.find().sort("created_at", -1):
                    items = []
                    if "items" in doc:
                        for item_data in doc["items"]:
                            items.append(ItemCotizacion(
                                material_id=item_data.get("material_id"),
                                nombre=item_data.get("nombre", ""),
                                cantidad=item_data.get("cantidad", 0),
                                precio_unitario=item_data.get("precio_unitario", 0),
                                subtotal=item_data.get("subtotal", 0)
                            ))
                    cotizaciones.append(Cotizacion(
                        id=str(doc.get("_id")),
                        cliente_nombre=doc.get("cliente_nombre", ""),
                        cliente_cedula=doc.get("cliente_cedula", ""),
                        items=items,
                        subtotal=doc.get("subtotal", 0),
                        itbms=doc.get("itbms", 0),
                        total=doc.get("total", 0),
                        sucursal=doc.get("sucursal", "CHIRIQUI"),
                        estado=doc.get("estado", "PENDIENTE"),
                        pdf_path=doc.get("pdf_path")
                    ))
                return cotizaciones
        except Exception as e:
            logger.error(f"Error obteniendo cotizaciones de MongoDB: {e}")
        
        return cotizaciones
    
    @staticmethod
    def get_by_id(cotizacion_id: str) -> Optional[Cotizacion]:
        """Obtiene una cotización por ID"""
        try:
            from bson.objectid import ObjectId
            collection = get_collection("cotizaciones")
            if collection is not None:
                doc = collection.find_one({"_id": ObjectId(cotizacion_id)})
                if doc:
                    items = []
                    if "items" in doc:
                        for item_data in doc["items"]:
                            items.append(ItemCotizacion(
                                material_id=item_data.get("material_id"),
                                nombre=item_data.get("nombre", ""),
                                cantidad=item_data.get("cantidad", 0),
                                precio_unitario=item_data.get("precio_unitario", 0),
                                subtotal=item_data.get("subtotal", 0)
                            ))
                    return Cotizacion(
                        id=str(doc.get("_id")),
                        cliente_nombre=doc.get("cliente_nombre", ""),
                        cliente_cedula=doc.get("cliente_cedula", ""),
                        items=items,
                        subtotal=doc.get("subtotal", 0),
                        itbms=doc.get("itbms", 0),
                        total=doc.get("total", 0),
                        sucursal=doc.get("sucursal", "CHIRIQUI"),
                        estado=doc.get("estado", "PENDIENTE"),
                        pdf_path=doc.get("pdf_path")
                    )
        except Exception as e:
            logger.error(f"Error obteniendo cotización: {e}")
        
        return None
    
    @staticmethod
    def update(cotizacion: Cotizacion) -> bool:
        """Actualiza una cotización"""
        try:
            from bson.objectid import ObjectId
            collection = get_collection("cotizaciones")
            if collection is not None:
                cotizacion.calcular_total()
                data = cotizacion.to_dict()
                data["items"] = [item.to_dict() for item in cotizacion.items]
                collection.update_one(
                    {"_id": ObjectId(cotizacion.id)},
                    {"$set": data}
                )
            return True
        except Exception as e:
            logger.error(f"Error actualizando cotización: {e}")
            return False
    
    @staticmethod
    def delete(cotizacion_id: str) -> bool:
        """Elimina una cotización"""
        try:
            from bson.objectid import ObjectId
            collection = get_collection("cotizaciones")
            if collection is not None:
                collection.delete_one({"_id": ObjectId(cotizacion_id)})
            return True
        except Exception as e:
            logger.error(f"Error eliminando cotización: {e}")
            return False
    
    @staticmethod
    def get_by_sucursal(sucursal: str) -> List[Cotizacion]:
        """Obtiene cotizaciones por sucursal"""
        cotizaciones = []
        try:
            collection = get_collection("cotizaciones")
            if collection is not None:
                for doc in collection.find({"sucursal": sucursal}):
                    items = []
                    if "items" in doc:
                        for item_data in doc["items"]:
                            items.append(ItemCotizacion(
                                material_id=item_data.get("material_id"),
                                nombre=item_data.get("nombre", ""),
                                cantidad=item_data.get("cantidad", 0),
                                precio_unitario=item_data.get("precio_unitario", 0),
                                subtotal=item_data.get("subtotal", 0)
                            ))
                    cotizaciones.append(Cotizacion(
                        id=str(doc.get("_id")),
                        cliente_nombre=doc.get("cliente_nombre", ""),
                        items=items,
                        total=doc.get("total", 0),
                        sucursal=doc.get("sucursal", "")
                    ))
        except Exception as e:
            logger.error(f"Error filtrando cotizaciones: {e}")
        
        return cotizaciones