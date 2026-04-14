# -*- coding: utf-8 -*-
"""
Validadores - Utilidades de Validación
Materiales Ibarra, S.A.
"""

import re
from typing import Any, Optional

class Validators:
    """Clase con métodos de validación"""
    
    @staticmethod
    def validate_not_empty(value: str) -> bool:
        """Valida que un campo no esté vacío"""
        if value is None:
            return False
        return len(str(value).strip()) > 0
    
    @staticmethod
    def validate_positive_number(value: float) -> bool:
        """Valida que sea un número positivo"""
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_positive_int(value: int) -> bool:
        """Valida que sea un entero positivo"""
        try:
            return int(value) > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_cedula(cedula: str) -> bool:
        """Valida formato de cédula PAN"""
        if not cedula:
            return True  # Opcional
        return bool(re.match(r'^\d{3}-\d{3}-\d{3}$|^\d{9,11}$', cedula))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        if not email:
            return True  # Opcional
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida formato de teléfono"""
        if not phone:
            return True  # Opcional
        return bool(re.match(r'^\+?[\d\s-]{7,15}$', phone))
    
    @staticmethod
    def validate_decimal_precision(value: float, precision: int = 2) -> float:
        """Redondea un decimal a la precisión especificada"""
        try:
            return round(float(value), precision)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def validate_in_range(value: float, min_val: float, max_val: float) -> bool:
        """Valida que un número esté en un rango"""
        try:
            return min_val <= float(value) <= max_val
        except (ValueError, TypeError):
            return False