# -*- coding: utf-8 -*-
"""
Servicio de Cotizaciones - Lógica de Negocio
Materiales Ibarra, S.A.
"""

from typing import List, Optional, Dict
from models.cotizacion import Cotizacion, ItemCotizacion
from models.material import Material
from repositories.cotizacion_repo import CotizacionRepository
from repositories.pdf_repo import PDFRepository
from services.pdf_service import PDFService
from utils.validators import Validators
import logging

logger = logging.getLogger(__name__)

class CotizacionService:
    """Servicio para gestión de cotizaciones"""
    
    @staticmethod
    def crear_cotizacion(cliente_nombre: str, cliente_cedula: str,
                        cliente_telefono: str, cliente_email: str,
                        items: List[Dict], sucursal: str = "CHIRIQUI") -> Optional[Cotizacion]:
        """Crea una nueva cotización"""
        try:
            if not Validators.validate_not_empty(cliente_nombre):
                raise ValueError("El nombre del cliente no puede estar vacío")
            if not items:
                raise ValueError("Debe agregar al menos un material a la cotización")
            
            cotizacion = Cotizacion(
                cliente_nombre=cliente_nombre.strip(),
                cliente_cedula=cliente_cedula.strip() if cliente_cedula else "",
                cliente_telefono=cliente_telefono.strip() if cliente_telefono else "",
                cliente_email=cliente_email.strip() if cliente_email else "",
                sucursal=sucursal
            )
            
            for item in items:
                material_id = item.get("material_id")
                cantidad = item.get("cantidad", 1)
                
                item_cotizacion = ItemCotizacion(
                    material_id=material_id,
                    nombre=item.get("nombre", ""),
                    cantidad=int(cantidad),
                    precio_unitario=float(item.get("precio", 0)),
                    subtotal=float(item.get("precio", 0)) * int(cantidad)
                )
                cotizacion.items.append(item_cotizacion)
            
            cotizacion.calcular_total()
            
            cotizacion_id = CotizacionRepository.create(cotizacion)
            if cotizacion_id:
                cotizacion.id = cotizacion_id
                logger.info(f"Cotización creada: {cotizacion.id}")
                return cotizacion
            
        except ValueError as ve:
            logger.warning(f"Validación fallida: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error creando cotización: {e}")
            raise
        
        return None
    
    @staticmethod
    def obtener_todas() -> List[Cotizacion]:
        """Obtiene todas las cotizaciones"""
        return CotizacionRepository.get_all()
    
    @staticmethod
    def obtener_por_id(cotizacion_id: int) -> Optional[Cotizacion]:
        """Obtiene una cotización por ID"""
        return CotizacionRepository.get_by_id(cotizacion_id)
    
    @staticmethod
    def obtener_por_sucursal(sucursal: str) -> List[Cotizacion]:
        """Obtiene cotizaciones filtradas por sucursal"""
        return CotizacionRepository.get_by_sucursal(sucursal)
    
    @staticmethod
    def actualizar_cotizacion(cotizacion: Cotizacion) -> bool:
        """Actualiza una cotización"""
        return CotizacionRepository.update(cotizacion)
    
    @staticmethod
    def eliminar_cotizacion(cotizacion_id: int) -> bool:
        """Elimina una cotización"""
        cotizacion = CotizacionRepository.get_by_id(cotizacion_id)
        if cotizacion and cotizacion.pdf_path:
            PDFRepository.delete_pdf(cotizacion.pdf_path)
        
        return CotizacionRepository.delete(cotizacion_id)
    
    @staticmethod
    def generar_pdf(cotizacion_id: int) -> Optional[str]:
        """Genera el PDF de una cotización"""
        try:
            cotizacion = CotizacionRepository.get_by_id(cotizacion_id)
            if not cotizacion:
                raise ValueError("Cotización no encontrada")
            
            pdf_bytes = PDFService.generar_cotizacion_pdf(cotizacion)
            if pdf_bytes:
                filename = f"cotizacion_{cotizacion_id}_{cotizacion.created_at.strftime('%Y%m%d_%H%M%S')}.pdf"
                ruta_pdf = PDFRepository.save_pdf(pdf_bytes, filename, "cotizacion")
                
                if ruta_pdf:
                    cotizacion.pdf_path = ruta_pdf
                    CotizacionRepository.update(cotizacion)
                    return ruta_pdf
            
            return None
            
        except Exception as e:
            logger.error(f"Error generando PDF: {e}")
            return None
    
    @staticmethod
    def convertir_a_factura(cotizacion_id: int, cedula: str, 
                            direccion: str, telefono: str) -> Optional[str]:
        """Convierte una cotización en factura fiscal"""
        try:
            cotizacion = CotizacionRepository.get_by_id(cotizacion_id)
            if not cotizacion:
                raise ValueError("Cotización no encontrada")
            
            # Importar aquí para evitar dependencia circular
            from services.facturacion_service import FacturacionService
            return FacturacionService.crear_factura_desde_cotizacion(
                cotizacion, cedula, direccion, telefono
            )
            
        except Exception as e:
            logger.error(f"Error convirtiendo a factura: {e}")
            return None