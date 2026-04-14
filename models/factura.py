# -*- coding: utf-8 -*-
"""
Modelo de Factura Fiscal (DGI)
Materiales Ibarra, S.A.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid
import hashlib

@dataclass
class ItemFactura:
    codigo: str
    descripcion: str
    cantidad: int
    precio_unitario: float
    itbms: float
    total: float
    
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
            "precio_unitario": round(self.precio_unitario, 2),
            "itbms": round(self.itbms, 2),
            "total": round(self.total, 2)
        }

@dataclass
class Factura:
    id: Optional[str] = None
    numero_factura: str = ""
    cedula_cliente: str = ""
    cliente_nombre: str = ""
    cliente_direccion: str = ""
    cliente_telefono: str = ""
    items: List[ItemFactura] = field(default_factory=list)
    subtotal: float = 0.0
    itbms: float = 0.0
    total: float = 0.0
    sucursal: str = "CHIRIQUI"
    estado: str = "ACTIVA"
    xml_dgi: str = ""
    pdf_path: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    @staticmethod
    def generar_numero_factura(sucursal: str) -> str:
        """Genera número de factura según formato DGI"""
        fecha = datetime.now().strftime("%Y%m%d")
        secuencia = str(uuid.uuid4())[:8].upper()
        return f"{sucursal}-{fecha}-{secuencia}"
    
    def calcular_total(self):
        """Calcula subtotal, ITBMS y total"""
        self.subtotal = sum(item.total for item in self.items)
        self.itbms = round(self.subtotal * 0.07, 2)
        self.total = round(self.subtotal + self.itbms, 2)
    
    def generar_xml_dgi(self) -> str:
        """Genera XML según formato DGI Panama"""
        self.calcular_total()
        
        items_xml = ""
        for item in self.items:
            items_xml += f"""
            <detalle>
                <codigo>{item.codigo}</codigo>
                <descripcion>{item.descripcion}</descripcion>
                <cantidad>{item.cantidad}</cantidad>
                <precioUnitario>{item.precio_unitario:.2f}</precioUnitario>
                <itbms>{item.itbms:.2f}</itbms>
                <total>{item.total:.2f}</total>
            </detalle>"""
        
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<facturaElectronica>
    <encabezado>
        <numeroFactura>{self.numero_factura}</numeroFactura>
        <fechaEmision>{self.created_at.strftime("%Y-%m-%dT%H:%M:%S")}</fechaEmision>
        <tipoDocumento>FACTURA</tipoDocumento>
        <tipoEmision>01</tipoEmision>
        <estado>ACTIVO</estado>
    </encabezado>
    <emisor>
        <razonSocial>Materiales Ibarra, S.A.</razonSocial>
        <ruc>XXXXXXXXXXXX</ruc>
        <direccion>Vía Panamericana, Chiriquí</direccion>
    </emisor>
    <receptor>
        <razonSocial>{self.cliente_nombre}</razonSocial>
        <ruc>{self.cedula_cliente}</ruc>
        <direccion>{self.cliente_direccion}</direccion>
        <telefono>{self.cliente_telefono}</telefono>
    </receptor>
    <items>{items_xml}
    </items>
    <totales>
        <subtotal>{self.subtotal:.2f}</subtotal>
        <itbms>{self.itbms:.2f}</itbms>
        <total>{self.total:.2f}</total>
    </totales>
    <firmaDigital>
        <hash>{hashlib.sha256(self.numero_factura.encode()).hexdigest()[:32]}</hash>
        <fechaFirma>{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}</fechaFirma>
    </firmaDigital>
</facturaElectronica>"""
        self.xml_dgi = xml
        return xml
    
    def to_dict(self):
        return {
            "id": self.id,
            "numero_factura": self.numero_factura,
            "cedula_cliente": self.cedula_cliente,
            "cliente_nombre": self.cliente_nombre,
            "cliente_direccion": self.cliente_direccion,
            "cliente_telefono": self.cliente_telefono,
            "items": [item.to_dict() for item in self.items],
            "subtotal": round(self.subtotal, 2),
            "itbms": round(self.itbms, 2),
            "total": round(self.total, 2),
            "sucursal": self.sucursal,
            "estado": self.estado,
            "xml_dgi": self.xml_dgi,
            "pdf_path": self.pdf_path,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }