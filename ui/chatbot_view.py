# -*- coding: utf-8 -*-
"""
Vista del Chatbot - Asistente Virtual
Materiales Ibarra, S.A.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from chatbot.bot import Chatbot
from services.stats_service import StatsService
from utils.logger import logger

class ChatbotView:
    """Vista del chatbot"""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Chatbot - Asistente Virtual")
        self.parent.geometry("600x500")
        
        self.chatbot = Chatbot()
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets de la vista"""
        header_frame = tk.Frame(self.parent, bg='#9b59b6', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="💬 Asistente Virtual - Materiales Ibarra",
                             font=('Arial', 14, 'bold'), bg='#9b59b6', fg='white')
        title_label.pack(pady=12)
        
        info_frame = tk.Frame(self.parent, bg='#ecf0f1')
        info_frame.pack(fill='x', padx=10, pady=5)
        
        stats_btn = ttk.Button(info_frame, text="📊 Ver Estadísticas", command=self.mostrar_estadisticas)
        stats_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(info_frame, text="🗑️ Limpiar Chat", command=self.limpiar_chat)
        clear_btn.pack(side='left', padx=5)
        
        chat_frame = ttk.Frame(self.parent, padding=10)
        chat_frame.pack(fill='both', expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(chat_frame, width=70, height=20,
                                                   font=('Courier', 10), wrap='word')
        self.chat_area.pack(fill='both', expand=True)
        self.chat_area.config(state='disabled')
        
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill='x', pady=10)
        
        self.entry_mensaje = ttk.Entry(input_frame, width=50, font=('Arial', 11))
        self.entry_mensaje.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_mensaje.bind('<Return>', lambda e: self.enviar_mensaje())
        
        btn_enviar = ttk.Button(input_frame, text="Enviar", command=self.enviar_mensaje)
        btn_enviar.pack(side='left')
        
        self.mostrar_mensaje("🤖", "¡Bienvenido a Materiales Ibarra, S.A.!\nSoy su asistente virtual. ¿En qué puedo ayudarle?\n\nEscriba 'ayuda' para ver los comandos disponibles.")
    
    def mostrar_mensaje(self, tipo: str, mensaje: str):
        """Muestra un mensaje en el chat"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{tipo} {mensaje}\n\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')
    
    def enviar_mensaje(self):
        """Envía un mensaje al chatbot"""
        mensaje = self.entry_mensaje.get().strip()
        if not mensaje:
            return
        
        self.mostrar_mensaje("👤", mensaje)
        self.entry_mensaje.delete(0, tk.END)
        
        try:
            respuesta = self.chatbot.process_message(mensaje)
            self.mostrar_mensaje("🤖", respuesta)
        except Exception as e:
            logger.error(f"Error en chatbot: {e}")
            self.mostrar_mensaje("🤖", "Disculpe, tuve un problema. Intente de nuevo.")
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas del sistema"""
        try:
            stats = StatsService.get_estadisticas_generales()
            mensaje = f"""📊 ESTADÍSTICAS DEL SISTEMA

✓ Total Materiales: {stats['total_materiales']}
✓ Total Cotizaciones: {stats['total_cotizaciones']}
✓ Total Facturas: {stats['total_facturas']}
✓ Ventas Totales: ${stats['ventas_totales']:.2f}

MATERIALES POR CATEGORÍA:"""
            
            for cat, cant in stats['materiales_por_categoria'].items():
                mensaje += f"\n  • {cat}: {cant}"
            
            mensaje += "\n\nCOTIZACIONES POR SUCURSAL:"
            for suc, cant in stats['cotizaciones_por_sucursal'].items():
                mensaje += f"\n  • {suc}: {cant}"
            
            self.mostrar_mensaje("📈", mensaje)
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            self.mostrar_mensaje("❌", "Error al obtener estadísticas")
    
    def limpiar_chat(self):
        """Limpia el chat"""
        self.chat_area.config(state='normal')
        self.chat_area.delete('1.0', tk.END)
        self.chat_area.config(state='disabled')
        self.chatbot.clear_historial()
        self.mostrar_mensaje("🤖", "Chat limpiado. ¿En qué puedo ayudar?")