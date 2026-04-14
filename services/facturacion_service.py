# -*- coding: utf-8 -*-
"""
Servicio de Facturación - Lógica de Negocio (DGI)
Materiales Ibarra, S.A.
"""

from typing import List, Optional
from bson.objectid import ObjectId
from models.factura import Factura, ItemFactura
from models.cotizacion import Cotizacion
from db.mongo import get_collection
from services.pdf_service import PDFService
from repositories.pdf_repo import PDFRepository
import logging

logger = logging.getLogger(__name__)

class FacturacionService:
    """Servicio para gestión de facturas fiscales"""
    
    @staticmethod
    def crear_factura(cedula: str, nombre: str, direccion: str, telefono: str,
                     items: List[dict], sucursal: str = "CHIRIQUI") -> Optional[Factura]:
        """Crea una nueva factura fiscal"""
        try:
            factura = Factura(
                numero_factura=Factura.generar_numero_factura(sucursal),
                cedula_cliente=cedula,
                cliente_nombre=nombre,
                cliente_direccion=direccion,
                cliente_telefono=telefono,
                sucursal=sucursal
            )
            
            for item in items:
                item_factura = ItemFactura(
                    codigo=str(item.get("material_id", "000")),
                    descripcion=item.get("nombre", "Producto"),
                    cantidad=int(item.get("cantidad", 1)),
                    precio_unitario=float(item.get("precio", 0)),
                    itbms=round(float(item.get("precio", 0)) * int(item.get("cantidad", 1)) * 0.07, 2),
                    total=round(float(item.get("precio", 0)) * int(item.get("cantidad", 1)) * 1.07, 2)
                )
                factura.items.append(item_factura)
            
            factura.calcular_total()
            factura.generar_xml_dgi()
            
            # Guardar en MongoDB
            collection = get_collection("facturas")
            if collection is not None:
                result = collection.insert_one(factura.to_dict())
                factura.id = str(result.inserted_id)
                logger.info(f"Factura guardada en MongoDB: {factura.numero_factura}")
            
            # Replicar a SQLite Chiriquí
            try:
                from db.sqlite_chiriqui import get_chiriqui_db
                conn = get_chiriqui_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO facturas (numero_factura, cedula_cliente, cliente_nombre, 
                            subtotal, itbms, total, sucursal, xml_dgi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (factura.numero_factura, factura.cedula_cliente, factura.cliente_nombre,
                          factura.subtotal, factura.itbms, factura.total, factura.sucursal, factura.xml_dgi))
                    conn.commit()
                    logger.info(f"Factura replicada en SQLite Chiriquí: {factura.numero_factura}")
            except Exception as e:
                logger.error(f"Error guardando en SQLite Chiriquí: {e}")
            
            # Replicar a SQLite Veraguas
            try:
                from db.sqlite_veraguas import get_veraguas_db
                conn = get_veraguas_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO facturas (numero_factura, cedula_cliente, cliente_nombre, 
                            subtotal, itbms, total, sucursal, xml_dgi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (factura.numero_factura, factura.cedula_cliente, factura.cliente_nombre,
                          factura.subtotal, factura.itbms, factura.total, factura.sucursal, factura.xml_dgi))
                    conn.commit()
                    logger.info(f"Factura replicada en SQLite Veraguas: {factura.numero_factura}")
            except Exception as e:
                logger.error(f"Error guardando en SQLite Veraguas: {e}")
            
            # Replicar a SQLite Chitré
            try:
                from db.sqlite_chitre import get_chitre_db
                conn = get_chitre_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO facturas (numero_factura, cedula_cliente, cliente_nombre, 
                            subtotal, itbms, total, sucursal, xml_dgi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (factura.numero_factura, factura.cedula_cliente, factura.cliente_nombre,
                          factura.subtotal, factura.itbms, factura.total, factura.sucursal, factura.xml_dgi))
                    conn.commit()
                    logger.info(f"Factura replicada en SQLite Chitré: {factura.numero_factura}")
            except Exception as e:
                logger.error(f"Error guardando en SQLite Chitré: {e}")
            
            return factura
        
        except Exception as e:
            logger.error(f"Error creando factura: {e}")
            return None
    
    @staticmethod
    def crear_factura_desde_cotizacion(cotizacion: Cotizacion, cedula: str,
                                       direccion: str, telefono: str) -> Optional[str]:
        """Convierte una cotización en factura fiscal y genera PDF"""
        try:
            items = []
            for item in cotizacion.items:
                items.append({
                    "material_id": item.material_id,
                    "nombre": item.nombre,
                    "cantidad": item.cantidad,
                    "precio": item.precio_unitario
                })
            
            factura = FacturacionService.crear_factura(
                cedula=cedula,
                nombre=cotizacion.cliente_nombre,
                direccion=direccion,
                telefono=telefono,
                items=items,
                sucursal=cotizacion.sucursal
            )
            
            if factura:
                pdf_bytes = PDFService.generar_factura_pdf(factura)
                if pdf_bytes:
                    filename = f"factura_{factura.numero_factura}.pdf"
                    ruta_pdf = PDFRepository.save_pdf(pdf_bytes, filename, "factura")
                    
                    # Guardar el pdf_path en la factura
                    if ruta_pdf and factura.id:
                        collection = get_collection("facturas")
                        if collection is not None:
                            collection.update_one(
                                {"_id": ObjectId(factura.id)},
                                {"$set": {"pdf_path": ruta_pdf}}
                            )
                            factura.pdf_path = ruta_pdf
                    
                    return ruta_pdf
            
            return None
            
        except Exception as e:
            logger.error(f"Error convirtiendo a factura: {e}")
            return None
    
    @staticmethod
    def obtener_todas() -> List[Factura]:
        """Obtiene todas las facturas desde MongoDB o SQLite"""
        facturas = []
        
        # Intentar desde MongoDB
        try:
            collection = get_collection("facturas")
            if collection is not None:
                for doc in collection.find().sort("created_at", -1):
                    items = []
                    if "items" in doc:
                        for item_data in doc["items"]:
                            items.append(ItemFactura(
                                codigo=item_data.get("codigo", ""),
                                descripcion=item_data.get("descripcion", ""),
                                cantidad=item_data.get("cantidad", 0),
                                precio_unitario=item_data.get("precio_unitario", 0),
                                itbms=item_data.get("itbms", 0),
                                total=item_data.get("total", 0)
                            ))
                    facturas.append(Factura(
                        id=str(doc.get("_id")),
                        numero_factura=doc.get("numero_factura", ""),
                        cedula_cliente=doc.get("cedula_cliente", ""),
                        cliente_nombre=doc.get("cliente_nombre", ""),
                        items=items,
                        subtotal=doc.get("subtotal", 0),
                        itbms=doc.get("itbms", 0),
                        total=doc.get("total", 0),
                        sucursal=doc.get("sucursal", ""),
                        pdf_path=doc.get("pdf_path", "")
                    ))
                return facturas
        except Exception as e:
            logger.error(f"Error obteniendo facturas de MongoDB: {e}")
        
        # Fallback a SQLite
        try:
            from db.sqlite_chiriqui import get_chiriqui_db
            conn = get_chiriqui_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM facturas ORDER BY created_at DESC")
                for row in cursor.fetchall():
                    facturas.append(Factura(
                        id=row["id"],
                        numero_factura=row["numero_factura"],
                        cedula_cliente=row["cedula_cliente"],
                        cliente_nombre=row["cliente_nombre"],
                        items=[],
                        subtotal=row["subtotal"],
                        itbms=row["itbms"],
                        total=row["total"],
                        sucursal=row["sucursal"]
                    ))
        except Exception as e:
            logger.error(f"Error obteniendo facturas de SQLite: {e}")
        
        return facturas
    
    @staticmethod
    def obtener_por_numero(numero: str) -> Optional[Factura]:
        """Obtiene una factura por número"""
        try:
            collection = get_collection("facturas")
            if collection is not None:
                doc = collection.find_one({"numero_factura": numero})
                if doc:
                    items = []
                    if "items" in doc:
                        for item_data in doc["items"]:
                            items.append(ItemFactura(
                                codigo=item_data.get("codigo", ""),
                                descripcion=item_data.get("descripcion", ""),
                                cantidad=item_data.get("cantidad", 0),
                                precio_unitario=item_data.get("precio_unitario", 0),
                                itbms=item_data.get("itbms", 0),
                                total=item_data.get("total", 0)
                            ))
                    return Factura(
                        id=str(doc.get("_id")),
                        numero_factura=doc.get("numero_factura", ""),
                        cedula_cliente=doc.get("cedula_cliente", ""),
                        cliente_nombre=doc.get("cliente_nombre", ""),
                        items=items,
                        subtotal=doc.get("subtotal", 0),
                        itbms=doc.get("itbms", 0),
                        total=doc.get("total", 0),
                        sucursal=doc.get("sucursal", ""),
                        pdf_path=doc.get("pdf_path", "")
                    )
        except Exception as e:
            logger.error(f"Error obteniendo factura: {e}")
        
        return None
    
    @staticmethod
    def generar_xml(factura: Factura) -> str:
        """Genera el XML DGI de una factura"""
        return factura.generar_xml_dgi()