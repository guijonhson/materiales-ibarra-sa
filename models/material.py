# -*- coding: utf-8 -*-
"""
Modelo de Materiales
Materiales Ibarra, S.A.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Material:
    id: Optional[str] = None
    nombre: str = ""
    descripcion: str = ""
    precio: float = 0.0
    cantidad: int = 0
    categoria: str = ""
    unidad: str = ""
    activo: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": round(self.precio, 2),
            "cantidad": self.cantidad,
            "categoria": self.categoria,
            "unidad": self.unidad,
            "activo": self.activo,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", ""),
            descripcion=data.get("descripcion", ""),
            # Soportar 'costo' (MongoDB) y 'precio' (SQLite/legacy)
            precio=float(data.get("costo") or data.get("precio") or 0),
            cantidad=int(data.get("cantidad", 0)),
            categoria=data.get("categoria", ""),
            unidad=data.get("unidad", ""),
            activo=data.get("activo", True),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )


class CategoriaMaterial:
    """Categorías disponibles para materiales"""
    CONSTRUCCION = "Construcción"
    HERRAMIENTAS = "Herramientas"
    PINTURAS = "Pinturas"
    ELECTRICOS = "Eléctricos"
    PLOMERIA = "Plomería"
    MADERA = "Madera"
    ACERO = "Acero"
    OTROS = "Otros"
    
    @staticmethod
    def get_all():
        return [
            CategoriaMaterial.CONSTRUCCION,
            CategoriaMaterial.HERRAMIENTAS,
            CategoriaMaterial.PINTURAS,
            CategoriaMaterial.ELECTRICOS,
            CategoriaMaterial.PLOMERIA,
            CategoriaMaterial.MADERA,
            CategoriaMaterial.ACERO,
            CategoriaMaterial.OTROS
        ]