# -*- coding: utf-8 -*-
"""
Motor NLP - Reglas de Procesamiento de Lenguaje Natural
Materiales Ibarra, S.A.
"""

import re
from typing import Dict, List

class NLPEngine:
    """Motor de procesamiento de lenguaje natural"""
    
    def __init__(self):
        self.intents = self._load_intents()
    
    def _load_intents(self) -> Dict[str, List[str]]:
        """Carga las intenciones y patrones"""
        return {
            "saludo": [
                "hola", "buenos días", "buenas tardes", "buenas noches",
                "buenas", "hola buenas", "hey", "wena", "qué tal",
                "cómo estás", "como estas", "saludos"
            ],
            "consulta_material": [
                "materiales", "productos", "catálogo", "catalogo",
                "qué venden", "tienen", "disponibles", "artículos",
                "articulos", "items", "mercancía", "mercancia"
            ],
            "precio": [
                "precio", "precios", "costo", "cuánto cuesta", "cuanto cuesta",
                "valor", "tarifa", "cuenta", "vale", "cuesta"
            ],
            "disponibilidad": [
                "disponible", "stock", "existe", "hay", "tienen en bodega",
                "existencia", "en existencia", "disponibilidad"
            ],
            "cotizacion": [
                "cotización", "cotizacion", "presupuesto", "presup",
                "cuánto sale", "cuanto sale", "presupuestar"
            ],
            "material_mas_cotizado": [
                "material más cotizado", "material mas cotizado",
                "producto más vendido", "producto mas vendido",
                "más solicitado", "mas solicitado", "top material",
                "material más popular", "material mas popular",
                "qué material", "cual material", "mejor material"
            ],
            "estadisticas": [
                "estadísticas", "estadisticas", "reporte", "reportes",
                "ventas", "cuántas ventas", "cantidad", "resumen"
            ],
            "ayuda": [
                "ayuda", "help", "comandos", "qué puedes hacer",
                "menu", "menú", "opciones", "qué делаешь"
            ],
            "despedida": [
                "adios", "adiós", "bye", "hasta luego", "nos vemos",
                "gracias", "chau", "hasta pronto", "me voy"
            ]
        }
    
    def detect_intent(self, message: str) -> str:
        """Detecta la intención del mensaje"""
        message = message.lower().strip()
        
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in message:
                    return intent
        
        return "default"
    
    def extract_entities(self, message: str) -> Dict[str, str]:
        """Extrae entidades del mensaje"""
        entities = {}
        
        material_match = re.search(r'(cemento|arena|grava|acero|bloque|varilla|pintura)', message.lower())
        if material_match:
            entities["material"] = material_match.group(1)
        
        cantidad_match = re.search(r'(\d+)\s*(unidades?|un|kg|libras?|bultos?)', message.lower())
        if cantidad_match:
            entities["cantidad"] = cantidad_match.group(1)
        
        precio_match = re.search(r'\$\s*(\d+)', message)
        if precio_match:
            entities["precio"] = precio_match.group(1)
        
        return entities
    
    def normalize_message(self, message: str) -> str:
        """Normaliza el mensaje"""
        message = message.lower().strip()
        message = re.sub(r'[^\w\s]', '', message)
        return message