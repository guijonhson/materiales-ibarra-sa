# -*- coding: utf-8 -*-
"""
Repositorio de Materiales - Capa de Acceso a Datos
Materiales Ibarra, S.A.
"""

from typing import List, Optional
from bson.objectid import ObjectId
from models.material import Material
from db.mongo import get_collection
from db.sqlite_chiriqui import get_chiriqui_db
from db.sqlite_veraguas import get_veraguas_db
from db.sqlite_chitre import get_chitre_db
import logging

logger = logging.getLogger(__name__)

class MaterialRepository:
    """Repositorio para gestión de materiales en todas las bases de datos"""
    
    @staticmethod
    def create(material: Material) -> Optional[str]:
        """Crea un nuevo material en MongoDB (principal) y SQLite"""
        # Error Crítico L20-72: Primero crear en MongoDB (fuente de verdad)
        mongo_id = None
        try:
            collection = get_collection("materiales")
            if collection is None:
                logger.error("MongoDB no disponible, no se puede crear material")
                return None
            
            result = collection.insert_one(material.to_dict())
            mongo_id = str(result.inserted_id)
            material.id = mongo_id
            logger.info(f"Material guardado en MongoDB: {mongo_id}")
            
            # Ahora replicar a SQLite (async sería mejor, pero por ahora síncrono)
            MaterialRepository._replicar_material_a_sqlite(material)
            
            return mongo_id
                 
        except Exception as e:
            logger.error(f"Error creando material: {e}")
            # Error Crítico L70-72: Si falló MongoDB, retornar None
            if mongo_id is None:
                return None
            # Si falló solo SQLite, retornar mongo_id pero logger.warning
            logger.warning(f"Material creado en MongoDB pero falló replicación a SQLite: {e}")
            return mongo_id
    
    @staticmethod
    def _replicar_material_a_sqlite(material: Material):
        """Replica un material a las 3 bases SQLite"""
        # Chiriquí
        try:
            conn = get_chiriqui_db()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO materiales (mongo_id, nombre, descripcion, precio, cantidad, categoria, unidad, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (material.id, material.nombre, material.descripcion, material.precio, 
                      material.cantidad, material.categoria, material.unidad, 1 if material.activo else 0))
                conn.commit()
                logger.info("Material replicado en Chiriquí")
        except Exception as e:
            logger.error(f"Error replicando a Chiriquí: {e}")
        
        # Veraguas
        try:
            conn = get_veraguas_db()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO materiales (mongo_id, nombre, descripcion, precio, cantidad, categoria, unidad, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (material.id, material.nombre, material.descripcion, material.precio, 
                      material.cantidad, material.categoria, material.unidad, 1 if material.activo else 0))
                conn.commit()
                logger.info("Material replicado en Veraguas")
        except Exception as e:
            logger.error(f"Error replicando a Veraguas: {e}")
        
        # Chitré
        try:
            conn = get_chitre_db()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO materiales (mongo_id, nombre, descripcion, precio, cantidad, categoria, unidad, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (material.id, material.nombre, material.descripcion, material.precio, 
                      material.cantidad, material.categoria, material.unidad, 1 if material.activo else 0))
                conn.commit()
                logger.info("Material replicado en Chitré")
        except Exception as e:
            logger.error(f"Error replicando a Chitré: {e}")
    
    @staticmethod
    def get_all() -> List[Material]:
        """Obtiene todos los materiales"""
        logger.info("=== MaterialRepository.get_all() START ===")
        materiales = []
        
        # Intentar desde MongoDB
        try:
            logger.info("Attempting to get collection 'materiales'...")
            collection = get_collection("materiales")
            logger.info(f"Got collection: {type(collection)}")
            
            if collection is not None:
                count = collection.count_documents({"activo": True})
                logger.info(f"MongoDB has {count} materials")
                for doc in collection.find({"activo": True}):
                    materiales.append(Material(
                        id=str(doc.get("_id")),
                        nombre=doc.get("nombre", ""),
                        descripcion=doc.get("descripcion", ""),
                        precio=doc.get("costo") or doc.get("precio") or 0,
                        cantidad=doc.get("cantidad", 0),
                        categoria=doc.get("categoria", ""),
                        unidad=doc.get("unidad", ""),
                        activo=doc.get("activo", True)
                    ))
                logger.info(f"Got {len(materiales)} from MongoDB, returning")
                return materiales
            else:
                logger.warning("Collection is None, trying SQLite")
        except Exception as e:
            logger.error(f"Error getting from MongoDB: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Fallback a SQLite
        try:
            conn = get_chiriqui_db()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM materiales WHERE activo = 1")
                for row in cursor.fetchall():
                    materiales.append(Material(
                        id=row["id"],
                        nombre=row["nombre"],
                        descripcion=row["descripcion"],
                        precio=row["precio"],
                        cantidad=row["cantidad"],
                        categoria=row["categoria"],
                        unidad=row["unidad"],
                        activo=bool(row["activo"])
                    ))
        except Exception as e:
            logger.error(f"Error obteniendo materiales de SQLite: {e}")
        
        return materiales
    
    @staticmethod
    def get_by_id(material_id: str) -> Optional[Material]:
        """Obtiene un material por ID"""
        # Error Bajo L124: Import movido al nivel del archivo
        try:
            collection = get_collection("materiales")
            if collection is not None:
                doc = collection.find_one({"_id": ObjectId(material_id)})
                if doc:
                    return Material(
                        id=str(doc.get("_id")),
                        nombre=doc.get("nombre", ""),
                        descripcion=doc.get("descripcion", ""),
                        precio=doc.get("costo") or doc.get("precio") or 0,
                        cantidad=doc.get("cantidad", 0),
                        categoria=doc.get("categoria", ""),
                        unidad=doc.get("unidad", "")
                    )
        except Exception as e:
            logger.error(f"Error obteniendo material: {e}")
        
        return None
    
    @staticmethod
    def update(material: Material) -> bool:
        """Actualiza un material en MongoDB y las 3 bases SQLite"""
        try:
            collection = get_collection("materiales")
            if collection is not None:
                collection.update_one(
                    {"_id": ObjectId(material.id)},
                    {"$set": material.to_dict()}
                )
                logger.info(f"Material actualizado en MongoDB: {material.id}")
            
            # Error Bajo L156-167: Actualizar las 3 bases SQLite
            # Chiriquí
            try:
                conn = get_chiriqui_db()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE materiales 
                        SET nombre=?, descripcion=?, precio=?, cantidad=?, 
                            categoria=?, unidad=?, updated_at=CURRENT_TIMESTAMP
                        WHERE mongo_id=?
                    """, (material.nombre, material.descripcion, material.precio,
                          material.cantidad, material.categoria, material.unidad, material.id))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error actualizando en Chiriquí: {e}")
            
            # Veraguas
            try:
                conn = get_veraguas_db()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE materiales 
                        SET nombre=?, descripcion=?, precio=?, cantidad=?, 
                            categoria=?, unidad=?, updated_at=CURRENT_TIMESTAMP
                        WHERE mongo_id=?
                    """, (material.nombre, material.descripcion, material.precio,
                          material.cantidad, material.categoria, material.unidad, material.id))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error actualizando en Veraguas: {e}")
            
            # Chitré
            try:
                conn = get_chitre_db()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE materiales 
                        SET nombre=?, descripcion=?, precio=?, cantidad=?, 
                            categoria=?, unidad=?, updated_at=CURRENT_TIMESTAMP
                        WHERE mongo_id=?
                    """, (material.nombre, material.descripcion, material.precio,
                          material.cantidad, material.categoria, material.unidad, material.id))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error actualizando en Chitré: {e}")
            
            return True
        except Exception as e:
            logger.error(f"Error actualizando material: {e}")
            return False
    
    @staticmethod
    def delete(material_id: str) -> bool:
        """Elimina (desactiva) un material en MongoDB y las 3 bases SQLite"""
        try:
            collection = get_collection("materiales")
            if collection is not None:
                collection.update_one(
                    {"_id": ObjectId(material_id)},
                    {"$set": {"activo": False}}
                )
            
            # Chiriquí
            try:
                conn = get_chiriqui_db()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE materiales SET activo = 0 WHERE mongo_id=?", (material_id,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error eliminando en Chiriquí: {e}")
            
            # Veraguas
            try:
                conn = get_veraguas_db()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE materiales SET activo = 0 WHERE mongo_id=?", (material_id,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error eliminando en Veraguas: {e}")
            
            # Chitré
            try:
                conn = get_chitre_db()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE materiales SET activo = 0 WHERE mongo_id=?", (material_id,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Error eliminando en Chitré: {e}")
            
            return True
        except Exception as e:
            logger.error(f"Error eliminando material: {e}")
            return False
    
    @staticmethod
    def get_by_categoria(categoria: str) -> List[Material]:
        """Obtiene materiales por categoría"""
        materiales = []
        try:
            collection = get_collection("materiales")
            if collection is not None:
                for doc in collection.find({"categoria": categoria, "activo": True}):
                    materiales.append(Material(
                        id=str(doc.get("_id")),
                        nombre=doc.get("nombre", ""),
                        descripcion=doc.get("descripcion", ""),
                        precio=doc.get("precio", 0),
                        cantidad=doc.get("cantidad", 0),
                        categoria=doc.get("categoria", ""),
                        unidad=doc.get("unidad", "")
                    ))
        except Exception as e:
            logger.error(f"Error filtrando por categoría: {e}")
        
        return materiales
    
    @staticmethod
    def search(query: str) -> List[Material]:
        """Busca materiales por nombre"""
        materiales = []
        try:
            collection = get_collection("materiales")
            if collection is not None:
                for doc in collection.find({
                    "$or": [
                        {"nombre": {"$regex": query, "$options": "i"}},
                        {"descripcion": {"$regex": query, "$options": "i"}}
                    ],
                    "activo": True
                }):
                    materiales.append(Material(
                        id=str(doc.get("_id")),
                        nombre=doc.get("nombre", ""),
                        descripcion=doc.get("descripcion", ""),
                        precio=doc.get("precio", 0),
                        cantidad=doc.get("cantidad", 0),
                        categoria=doc.get("categoria", ""),
                        unidad=doc.get("unidad", "")
                    ))
        except Exception as e:
            logger.error(f"Error buscando materiales: {e}")
        
        return materiales