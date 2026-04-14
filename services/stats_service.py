# -*- coding: utf-8 -*-
"""
Servicio de Estadísticas
Materiales Ibarra, S.A.
"""

from typing import Dict, List
from db.mongo import get_collection
from repositories.material_repo import MaterialRepository
from repositories.cotizacion_repo import CotizacionRepository
import logging

logger = logging.getLogger(__name__)

class StatsService:
    """Servicio para obtener estadísticas del sistema"""
    
    @staticmethod
    def get_total_materiales() -> int:
        """Obtiene el total de materiales"""
        try:
            collection = get_collection("materiales")
            if collection is not None:
                return collection.count_documents({"activo": True})
        except Exception as e:
            logger.error(f"Error obteniendo total materiales: {e}")
        return 0
    
    @staticmethod
    def get_total_cotizaciones() -> int:
        """Obtiene el total de cotizaciones"""
        try:
            collection = get_collection("cotizaciones")
            if collection is not None:
                return collection.count_documents({})
        except Exception as e:
            logger.error(f"Error obteniendo total cotizaciones: {e}")
        return 0
    
    @staticmethod
    def get_total_facturas() -> int:
        """Obtiene el total de facturas"""
        try:
            collection = get_collection("facturas")
            if collection is not None:
                return collection.count_documents({})
        except Exception as e:
            logger.error(f"Error obteniendo total facturas: {e}")
        return 0
    
    @staticmethod
    def get_ventas_totales() -> float:
        """Obtiene el total de ventas"""
        try:
            collection = get_collection("facturas")
            if collection is not None:
                pipeline = [{"$group": {"_id": None, "total": {"$sum": "$total"}}}]
                result = list(collection.aggregate(pipeline))
                if result:
                    return result[0].get("total", 0)
        except Exception as e:
            logger.error(f"Error obteniendo ventas: {e}")
        return 0.0
    
    @staticmethod
    def get_materiales_por_categoria() -> Dict[str, int]:
        """Obtiene cantidad de materiales por categoría"""
        try:
            collection = get_collection("materiales")
            if collection is not None:
                pipeline = [
                    {"$match": {"activo": True}},
                    {"$group": {"_id": "$categoria", "total": {"$sum": 1}}}
                ]
                result = collection.aggregate(pipeline)
                return {doc["_id"]: doc["total"] for doc in result}
        except Exception as e:
            logger.error(f"Error obteniendo categorías: {e}")
        return {}
    
    @staticmethod
    def get_top_materiales(limit: int = 10) -> List[Dict]:
        """Obtiene los materiales más cotizados/vendidos"""
        try:
            collection = get_collection("cotizaciones")
            if collection is not None:
                pipeline = [
                    {"$unwind": "$items"},
                    {"$group": {"_id": "$items.material_id", "nombre": {"$first": "$items.nombre"}, "cantidad": {"$sum": "$items.cantidad"}}},
                    {"$sort": {"cantidad": -1}},
                    {"$limit": limit}
                ]
                result = collection.aggregate(pipeline)
                return [{"material_id": doc["_id"], "nombre": doc["nombre"], "cantidad": doc["cantidad"]} for doc in result]
        except Exception as e:
            logger.error(f"Error obteniendo top materiales: {e}")
        return []
    
    @staticmethod
    def get_cotizaciones_por_sucursal() -> Dict[str, int]:
        """Obtiene cotizaciones por sucursal"""
        try:
            collection = get_collection("cotizaciones")
            if collection is not None:
                pipeline = [
                    {"$group": {"_id": "$sucursal", "total": {"$sum": 1}}}
                ]
                result = collection.aggregate(pipeline)
                return {doc["_id"]: doc["total"] for doc in result}
        except Exception as e:
            logger.error(f"Error obteniendo cotizaciones por sucursal: {e}")
        return {}
    
    @staticmethod
    def get_estadisticas_generales() -> Dict:
        """Obtiene un resumen de todas las estadísticas"""
        return {
            "total_materiales": StatsService.get_total_materiales(),
            "total_cotizaciones": StatsService.get_total_cotizaciones(),
            "total_facturas": StatsService.get_total_facturas(),
            "ventas_totales": round(StatsService.get_ventas_totales(), 2),
            "materiales_por_categoria": StatsService.get_materiales_por_categoria(),
            "cotizaciones_por_sucursal": StatsService.get_cotizaciones_por_sucursal()
        }