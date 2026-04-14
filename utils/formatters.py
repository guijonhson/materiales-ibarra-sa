# -*- coding: utf-8 -*-
"""
Formateadores - Utilidades de Formato
Materiales Ibarra, S.A.
"""

from datetime import datetime
from typing import Any

class Formatters:
    """Clase con métodos de formato"""
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Formatea un valor como moneda"""
        return f"${value:,.2f}"
    
    @staticmethod
    def format_decimal(value: float, decimals: int = 2) -> str:
        """Formatea un decimal con cifras significativas"""
        return f"{value:.{decimals}f}"
    
    @staticmethod
    def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
        """Formatea una fecha"""
        if date:
            return date.strftime(format_str)
        return ""
    
    @staticmethod
    def format_datetime(date: datetime) -> str:
        """Formatea fecha y hora"""
        if date:
            return date.strftime("%Y-%m-%d %H:%M:%S")
        return ""
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Formatea un número de teléfono"""
        if not phone:
            return ""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return phone
    
    @staticmethod
    def format_cedula(cedula: str) -> str:
        """Formatea una cédula PAN"""
        if not cedula:
            return ""
        digits = ''.join(filter(str.isdigit, cedula))
        if len(digits) == 9:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        return cedula
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 50) -> str:
        """Trunca texto a una longitud máxima"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    @staticmethod
    def format_sucursal(codigo: str) -> str:
        """Formatea el código de sucursal"""
        sucursales = {
            "CH": "Chiriquí",
            "VR": "Veraguas", 
            "CT": "Chitré"
        }
        return sucursales.get(codigo, codigo)