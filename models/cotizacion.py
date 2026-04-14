# -*- coding: utf-8 -*-
"""
Modelo de Cotización
Materiales Ibarra, S.A.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import json

@dataclass
class ItemCotizacion:
    material_id: int
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float
    
    def to_dict(self):
        return {
            "material_id": self.material_id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": round(self.precio_unitario, 2),
            "subtotal": round(self.subtotal, 2)
        }

@dataclass
class Cotizacion:
    id: Optional[str] = None
    cliente_nombre: str = ""
    cliente_cedula: str = ""
    cliente_telefono: str = ""
    cliente_email: str = ""
    items: List[ItemCotizacion] = field(default_factory=list)
    subtotal: float = 0.0
    itbms: float = 0.0
    total: float = 0.0
    sucursal: str = "CHIRIQUI"
    estado: str = "PENDIENTE"
    pdf_path: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calcular_total(self):
        """Calcula el subtotal, ITBMS y total de la cotización"""
        self.subtotal = sum(item.subtotal for item in self.items)
        self.itbms = round(self.subtotal * 0.07, 2)  # 7% ITBMS
        self.total = round(self.subtotal + self.itbms, 2)
    
    def to_dict(self):
        return {
            "id": self.id,
            "cliente_nombre": self.cliente_nombre,
            "cliente_cedula": self.cliente_cedula,
            "cliente_telefono": self.cliente_telefono,
            "cliente_email": self.cliente_email,
            "items": [item.to_dict() for item in self.items],
            "subtotal": round(self.subtotal, 2),
            "itbms": round(self.itbms, 2),
            "total": round(self.total, 2),
            "sucursal": self.sucursal,
            "estado": self.estado,
            "pdf_path": self.pdf_path,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data):
        items = []
        if "items" in data and data["items"]:
            for item_data in data["items"]:
                items.append(ItemCotizacion(
                    material_id=item_data.get("material_id"),
                    nombre=item_data.get("nombre", ""),
                    cantidad=item_data.get("cantidad", 0),
                    precio_unitario=item_data.get("precio_unitario", 0),
                    subtotal=item_data.get("subtotal", 0)
                ))
        return cls(
            id=data.get("id"),
            cliente_nombre=data.get("cliente_nombre", ""),
            cliente_cedula=data.get("cliente_cedula", ""),
            cliente_telefono=data.get("cliente_telefono", ""),
            cliente_email=data.get("cliente_email", ""),
            items=items,
            subtotal=data.get("subtotal", 0),
            itbms=data.get("itbms", 0),
            total=data.get("total", 0),
            sucursal=data.get("sucursal", "CHIRIQUI"),
            estado=data.get("estado", "PENDIENTE"),
            pdf_path=data.get("pdf_path"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )