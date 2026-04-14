# -*- coding: utf-8 -*-
"""
Servicio de Replicación - Sincronización entre Sucursales
Materiales Ibarra, S.A.
"""

import threading
import time
import json
from db.mongo import get_collection
from db.sqlite_chiriqui import get_chiriqui_db
from db.sqlite_veraguas import get_veraguas_db
from db.sqlite_chitre import get_chitre_db
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class ReplicacionService:
    """Servicio para replicar datos entre sucursales"""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Inicia el hilo de replicación"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._replicar_loop, daemon=True)
            self.thread.start()
            logger.info("✓ Servicio de replicación iniciado")
    
    def stop(self):
        """Detiene el hilo de replicación"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("✗ Servicio de replicación detenido")
    
    def _replicar_loop(self):
        """Bucle principal de replicación"""
        while self.running:
            try:
                self.replicar_materiales()
                self.replicar_cotizaciones()
                self.replicar_facturas()
                # Error Alto L40-49: Leer intervalo de Config
                time.sleep(Config.REPLICACION_INTERVAL)
            except Exception as e:
                logger.error(f"Error en bucle de replicación: {e}")
    
    def replicar_materiales(self):
        """Replica materiales de MongoDB a SQLite"""
        try:
            collection = get_collection("materiales")
            if collection is None:
                logger.warning("MongoDB no disponible para replicar materiales")
                return
            
            materiales = list(collection.find({"activo": True}))
            
            # Replicar a Chiriquí
            conn_ch = get_chiriqui_db()
            if conn_ch is not None:
                cursor = conn_ch.cursor()
                cursor.execute("DELETE FROM materiales")  # Limpiar antes de replicar
                for mat in materiales:
                    nombre = mat.get("nombre", "")
                    desc = mat.get("descripcion", "")
                    # MongoDB usa 'costo', SQLite usa 'precio'
                    precio = mat.get("costo") or mat.get("precio") or 0
                    cantidad = mat.get("cantidad") or 0
                    categoria = mat.get("categoria", "") or "General"
                    unidad = mat.get("unidad", "UND") or "UND"
                    
                    cursor.execute("""
                        INSERT INTO materiales 
                        (mongo_id, nombre, descripcion, precio, cantidad, categoria, unidad, activo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                    """, (str(mat.get("_id")), nombre, desc, precio, cantidad, categoria, unidad))
                conn_ch.commit()
                logger.info(f"✓ Materiales replicados a Chiriquí: {len(materiales)}")
            
            # Replicar a Veraguas
            conn_vr = get_veraguas_db()
            if conn_vr is not None:
                cursor = conn_vr.cursor()
                cursor.execute("DELETE FROM materiales")
                for mat in materiales:
                    nombre = mat.get("nombre", "")
                    desc = mat.get("descripcion", "")
                    precio = mat.get("costo") or mat.get("precio") or 0
                    cantidad = mat.get("cantidad") or 0
                    categoria = mat.get("categoria", "") or "General"
                    unidad = mat.get("unidad", "UND") or "UND"
                    
                    cursor.execute("""
                        INSERT INTO materiales 
                        (mongo_id, nombre, descripcion, precio, cantidad, categoria, unidad, activo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                    """, (str(mat.get("_id")), nombre, desc, precio, cantidad, categoria, unidad))
                conn_vr.commit()
                logger.info(f"✓ Materiales replicados a Veraguas: {len(materiales)}")
                
        except Exception as e:
            logger.error(f"Error replicando materiales: {e}")
    
    def replicar_cotizaciones(self):
        """Replica cotizaciones entre bases de datos"""
        try:
            collection = get_collection("cotizaciones")
            if collection is None:
                logger.warning("MongoDB no disponible para replicar cotizaciones")
                return
            
            cotizaciones = list(collection.find())
            
            # Replicar a Chiriquí - Error Alto L122-133: Usar json.dumps/loads correctamente
            conn_ch = get_chiriqui_db()
            if conn_ch is not None:
                cursor = conn_ch.cursor()
                for cot in cotizaciones:
                    materiales_json = json.dumps(cot.get("materiales", []))
                    cursor.execute("""
                        INSERT OR REPLACE INTO cotizaciones 
                        (mongo_id, cliente_nombre, cliente_cedula, materiales, total, sucursal, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (str(cot.get("_id")), cot.get("cliente_nombre"), 
                          cot.get("cliente_cedula"), materiales_json,
                          cot.get("total", 0), cot.get("sucursal", "CHIRIQUI"),
                          cot.get("estado", "PENDIENTE")))
                conn_ch.commit()
                logger.debug("✓ Cotizaciones replicadas a Chiriquí")
            
            # Replicar a Veraguas
            conn_vr = get_veraguas_db()
            if conn_vr is not None:
                cursor = conn_vr.cursor()
                for cot in cotizaciones:
                    materiales_json = json.dumps(cot.get("materiales", []))
                    cursor.execute("""
                        INSERT OR REPLACE INTO cotizaciones 
                        (mongo_id, cliente_nombre, cliente_cedula, materiales, total, sucursal, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (str(cot.get("_id")), cot.get("cliente_nombre"), 
                          cot.get("cliente_cedula"), materiales_json,
                          cot.get("total", 0), cot.get("sucursal", "VERAGUAS"),
                          cot.get("estado", "PENDIENTE")))
                conn_vr.commit()
                logger.debug("✓ Cotizaciones replicadas a Veraguas")
            
            # Replicar a Chitré
            conn_ct = get_chitre_db()
            if conn_ct is not None:
                cursor = conn_ct.cursor()
                for cot in cotizaciones:
                    materiales_json = json.dumps(cot.get("materiales", []))
                    cursor.execute("""
                        INSERT OR REPLACE INTO cotizaciones 
                        (mongo_id, cliente_nombre, cliente_cedula, materiales, total, sucursal, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (str(cot.get("_id")), cot.get("cliente_nombre"), 
                          cot.get("cliente_cedula"), materiales_json,
                          cot.get("total", 0), cot.get("sucursal", "CHITRE"),
                          cot.get("estado", "PENDIENTE")))
                conn_ct.commit()
                logger.debug("✓ Cotizaciones replicadas a Chitré")
                    
        except Exception as e:
            logger.error(f"Error replicando cotizaciones: {e}")
    
    def replicar_facturas(self):
        """Replica facturas entre bases de datos"""
        try:
            collection = get_collection("facturas")
            if collection is None:
                logger.warning("MongoDB no disponible para replicar facturas")
                return
            
            facturas = list(collection.find())
            
            # Replicar a Chiriquí - Error Medio L186-197: Cambiar a INSERT OR REPLACE
            conn_ch = get_chiriqui_db()
            if conn_ch is not None:
                cursor = conn_ch.cursor()
                for fac in facturas:
                    cursor.execute("""
                        INSERT OR REPLACE INTO facturas 
                        (mongo_id, numero_factura, cedula_cliente, cliente_nombre, subtotal, itbms, total, sucursal, xml_dgi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (str(fac.get("_id")), fac.get("numero_factura"), fac.get("cedula_cliente"),
                          fac.get("cliente_nombre"), fac.get("subtotal", 0),
                          fac.get("itbms", 0), fac.get("total", 0),
                          fac.get("sucursal", "CHIRIQUI"), fac.get("xml_dgi", "")))
                conn_ch.commit()
                logger.debug("✓ Facturas replicadas a Chiriquí")
            
            # Replicar a Veraguas
            conn_vr = get_veraguas_db()
            if conn_vr is not None:
                cursor = conn_vr.cursor()
                for fac in facturas:
                    cursor.execute("""
                        INSERT OR REPLACE INTO facturas 
                        (mongo_id, numero_factura, cedula_cliente, cliente_nombre, subtotal, itbms, total, sucursal, xml_dgi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (str(fac.get("_id")), fac.get("numero_factura"), fac.get("cedula_cliente"),
                          fac.get("cliente_nombre"), fac.get("subtotal", 0),
                          fac.get("itbms", 0), fac.get("total", 0),
                          fac.get("sucursal", "VERAGUAS"), fac.get("xml_dgi", "")))
                conn_vr.commit()
                logger.debug("✓ Facturas replicadas a Veraguas")
            
            # Replicar a Chitré
            conn_ct = get_chitre_db()
            if conn_ct is not None:
                cursor = conn_ct.cursor()
                for fac in facturas:
                    cursor.execute("""
                        INSERT OR REPLACE INTO facturas 
                        (mongo_id, numero_factura, cedula_cliente, cliente_nombre, subtotal, itbms, total, sucursal, xml_dgi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (str(fac.get("_id")), fac.get("numero_factura"), fac.get("cedula_cliente"),
                          fac.get("cliente_nombre"), fac.get("subtotal", 0),
                          fac.get("itbms", 0), fac.get("total", 0),
                          fac.get("sucursal", "CHITRE"), fac.get("xml_dgi", "")))
                conn_ct.commit()
                logger.debug("✓ Facturas replicadas a Chitré")
                    
        except Exception as e:
            logger.error(f"Error replicando facturas: {e}")
    
    def forzar_sincronizacion(self):
        """Fuerza una sincronización inmediata"""
        self.replicar_materiales()
        self.replicar_cotizaciones()
        self.replicar_facturas()
        logger.info("✓ Sincronización forzada completada")

replicacion_service = ReplicacionService()