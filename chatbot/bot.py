# -*- coding: utf-8 -*-
"""
Chatbot - Motor del Asistente Virtual
Materiales Ibarra, S.A.
"""

import time
from chatbot.nlp_rules import NLPEngine
from services.stats_service import StatsService
from models.material import Material
from repositories.material_repo import MaterialRepository
import logging

logger = logging.getLogger(__name__)

class Chatbot:
    """Chatbot para atención al cliente"""
    
    def __init__(self):
        self.nlp = NLPEngine()
        self.historial = []
        self.context = {}
        # Error Medio L87-93: Implementar caché con TTL de 30 segundos
        self._stats_cache = None
        self._stats_cache_time = 0
        self._stats_cache_ttl = 30
    
    def process_message(self, message: str) -> str:
        """Procesa un mensaje del usuario"""
        # Error Medio L38-50: Agregar logging de intent no reconocido
        try:
            intent = self.nlp.detect_intent(message.lower())
            if intent == "desconocido":
                logger.debug(f"Intent no reconocido: {message}")
            response = self._generate_response(intent, message)
            
            # Error Medio L23-34: Agregar límite de tamaño del historial
            if len(self.historial) > 100:
                self.historial.pop(0)
            
            self.historial.append({"user": message, "bot": response})
            return response
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return "Disculpe, tuve un problema al procesar su mensaje. ¿Podría reformularlo?"
    
    def _generate_response(self, intent: str, message: str) -> str:
        """Genera una respuesta basada en la intención"""
        responses = {
            "saludo": self._handle_saludo,
            "consulta_material": self._handle_consulta_material,
            "precio": self._handle_precio,
            "disponibilidad": self._handle_disponibilidad,
            "cotizacion": self._handle_cotizacion,
            "estadisticas": self._handle_estadisticas,
            "ayuda": self._handle_ayuda,
            "despedida": self._handle_despedida,
            "material_mas_cotizado": self._handle_material_mas_cotizado,
            "desconocido": self._handle_default
        }
        
        handler = responses.get(intent, self._handle_default)
        return handler(message)
    
    def _handle_saludo(self, message: str) -> str:
        return ("¡Bienvenido a Materiales Ibarra, S.A.!\n"
                "Soy su asistente virtual. ¿En qué puedo ayudarle hoy?\n"
                "- Consultar materiales disponibles\n"
                "- Ver precios\n"
                "- Realizar una cotización\n"
                "- Consultar disponibilidad de productos\n"
                "- Ver material más cotizado")
    
    def _handle_consulta_material(self, message: str) -> str:
        materiales = MaterialRepository.get_all()
        if materiales:
            lista = "\n".join([f"• {m.nombre} - ${m.precio:.2f}" for m in materiales[:10]])
            return f"Materiales disponibles:\n{lista}\n\nPara más información, contacte a un asesor."
        return "No hay materiales disponibles en este momento."
    
    def _handle_precio(self, message: str) -> str:
        materiales = MaterialRepository.get_all()
        if materiales:
            return f"Los precios oscilan entre ${min(m.precio for m in materiales):.2f} y ${max(m.precio for m in materiales):.2f}"
        return "No hay materiales disponibles."
    
    def _handle_disponibilidad(self, message: str) -> str:
        materiales = MaterialRepository.get_all()
        disponibles = [m for m in materiales if m.cantidad > 0]
        if disponibles:
            lista = "\n".join([f"• {m.nombre}: {m.cantidad} {m.unidad}" for m in disponibles[:10]])
            return f"Productos en stock:\n{lista}"
        return "No hay productos en stock actualmente."
    
    def _handle_cotizacion(self, message: str) -> str:
        return ("Para realizar una cotización, puede:\n"
                "1. Acudir directamente a cualquiera de nuestras sucursales\n"
                "2. Llamar a nuestros números de contacto\n"
                "3. Utilizar la opción de 'Cliente' en nuestro sistema")
    
    def _handle_material_mas_cotizado(self, message: str) -> str:
        """Error Medio L60-65: Agregar handler específico para material más cotizado"""
        try:
            top_materiales = StatsService.get_top_materiales(limit=5)
            if top_materiales:
                lista = "\n".join([f"• {m['nombre']}: {m['cantidad']} unidades" for m in top_materiales])
                return f"📊 Materiales más cotizados:\n{lista}"
            return "No hay datos de materiales más cotizados."
        except Exception as e:
            logger.error(f"Error obteniendo top materiales: {e}")
            return "Disculpe, no pude obtener los materiales más cotizados."
    
    def _handle_estadisticas(self, message: str) -> str:
        """Error Medio L87-93: Usar caché con TTL de 30 segundos"""
        current_time = time.time()
        
        # Verificar si el caché es válido
        if self._stats_cache is not None and (current_time - self._stats_cache_time) < self._stats_cache_ttl:
            stats = self._stats_cache
        else:
            # Obtener nuevas estadísticas y actualizar caché
            try:
                stats = StatsService.get_estadisticas_generales()
                self._stats_cache = stats
                self._stats_cache_time = current_time
            except Exception as e:
                logger.error(f"Error obteniendo estadísticas: {e}")
                return "Disculpe, no pude obtener las estadísticas del sistema."
        
        return (f"📊 Estadísticas del Sistema:\n"
                f"• Total Materiales: {stats['total_materiales']}\n"
                f"• Cotizaciones: {stats['total_cotizaciones']}\n"
                f"• Facturas: {stats['total_facturas']}\n"
                f"• Ventas Totales: ${stats['ventas_totales']:.2f}")
    
    def _handle_ayuda(self, message: str) -> str:
        return ("Comandos disponibles:\n"
                "- 'materiales': Ver lista de materiales\n"
                "- 'precios': Consultar rango de precios\n"
                "- 'stock': Ver disponibilidad\n"
                "- 'material más cotizado': Ver productos más solicitados\n"
                "- 'cotización': Cómo realizar una cotización\n"
                "- 'estadísticas': Ver estadísticas del sistema\n"
                "- 'ayuda': Ver este menú")
    
    def _handle_despedida(self, message: str) -> str:
        return ("¡Gracias por contactarnos!\n"
                "Recuerde que estamos para servirle en cualquiera de nuestras sucursales:\n"
                "• Chiriquí: Vía Panamericana\n"
                "• Veraguas: Frente al Mall de Santiago\n"
                "• Chitré: Frente al Hotel Gran Azuero\n"
                "¡Hasta pronto!")
    
    def _handle_default(self, message: str) -> str:
        return ("No entendí completamente su consulta. "
                "Escriba 'ayuda' para ver las opciones disponibles.")
    
    def get_historial(self) -> list:
        """Retorna el historial de conversaciones"""
        return self.historial
    
    def clear_historial(self):
        """Limpia el historial"""
        self.historial = []
        # También limpiar caché
        self._stats_cache = None