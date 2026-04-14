# -*- coding: utf-8 -*-
"""
Interfaz Gráfica Principal - Aplicación Materiales Ibarra
Materiales Ibarra, S.A.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.admin_view import AdminView
from ui.cliente_view import ClienteView
from ui.chatbot_view import ChatbotView
from db.connection_manager import connection_manager
from services.replicacion_service import replicacion_service
from utils.logger import logger
import sys

class AppUI:
    """Interfaz gráfica principal de la aplicación"""
    
    def __init__(self):
        print("STDOUT: AppUI.__init__ called", flush=True)
        self.root = tk.Tk()
        self.root.title("Materiales Ibarra, S.A. - Sistema de Gestión")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.style_config()
        self.create_menu()
        self.create_main_layout()
        
        self.inicializar_base_datos()
    
    def style_config(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), background='#2C3E50', foreground='white')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        style.configure('Info.TLabel', font=('Arial', 9), background='#f0f0f0', foreground='#666')
        
        style.map('TButton', background=[('active', '#3498db')])
    
    def create_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Inicializar BD", command=self.inicializar_base_datos)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.salir)
        
        menu_sucursales = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sucursales", menu=menu_sucursales)
        menu_sucursales.add_command(label="Ver Conexiones", command=self.ver_conexiones)
        menu_sucursales.add_command(label="Forzar Sincronización", command=self.forzar_sincronizacion)
        
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca)
    
    def create_main_layout(self):
        """Crea el layout principal"""
        self.root.configure(bg='#f0f0f0')
        
        header_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="MATERIALES IBARRA, S.A.", 
                               font=('Arial', 20, 'bold'), bg='#2C3E50', fg='white')
        title_label.pack(pady=10)
        
        subtitle = tk.Label(header_frame, text="Sistema de Gestión Integral", 
                           font=('Arial', 10), bg='#2C3E50', fg='#bdc3c7')
        subtitle.pack()
        
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        self.create_buttons(main_frame)
        
        status_frame = tk.Frame(self.root, bg='#34495e', height=40)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Sistema Listo", 
                                     font=('Arial', 9), bg='#34495e', fg='white')
        self.status_label.pack(pady=10)
    
    def create_buttons(self, parent):
        """Crea los botones principales"""
        print("STDOUT: create_buttons called", flush=True)
        
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill='both', expand=True, pady=20)
        
        ttk.Label(btn_frame, text="Seleccione su rol:", style='Title.TLabel').pack(pady=10)
        
        admin_btn = tk.Button(btn_frame, text="👥 ADMINISTRADOR", 
                             command=self.abrir_admin, width=30, height=2)
        admin_btn.pack(pady=10)
        admin_btn.configure(font=('Arial', 12, 'bold'), bg='#3498db', fg='white', relief='flat')
        
        cliente_btn = tk.Button(btn_frame, text="🛒 CLIENTE - Cotizaciones", 
                               command=self.abrir_cliente, width=30, height=2)
        cliente_btn.pack(pady=10)
        cliente_btn.configure(font=('Arial', 12, 'bold'), bg='#27ae60', fg='white', relief='flat')
        
        chatbot_btn = tk.Button(btn_frame, text="💬 CHATBOT - Asistente Virtual", 
                               command=self.abrir_chatbot, width=30, height=2)
        chatbot_btn.pack(pady=10)
        chatbot_btn.configure(font=('Arial', 12, 'bold'), bg='#9b59b6', fg='white', relief='flat')
        
        for btn in [admin_btn, cliente_btn, chatbot_btn]:
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#2980b9'))
            btn.bind('<Leave>', lambda e, b=btn, c={'#3498db':'#2980b9', '#27ae60':'#1e8449', '#9b59b6':'#8e44ad'}: 
                    b.configure(bg=c.get(btn.cget('bg'), '#3498db')))
    
    def inicializar_base_datos(self):
        """Inicializa las conexiones a las bases de datos"""
        try:
            self.status_label.config(text="Conectando a bases de datos...")
            self.root.update()
            
            connection_manager.initialize_all()
            replicacion_service.start()
            
            status = connection_manager.get_status()
            # Error Medio app_ui.py L122-141: Validar resultado de initialize_all
            if not status['mongodb']:
                messagebox.showwarning("Advertencia", "MongoDB no disponible. Usando SQLite como respaldo.")
            
            status_text = f"Conectado - MongoDB: {'✓' if status['mongodb'] else '✗'} | "
            status_text += f"Chiriquí: {'✓' if status['chiriqui'] else '✗'} | "
            status_text += f"Veraguas: {'✓' if status['veraguas'] else '✗'}"
            
            self.status_label.config(text=status_text)
            logger.info("Bases de datos inicializadas correctamente")
            
            # Error Alto: Verificar que SQLite también esté disponible
            if not status['chiriqui'] or not status['veraguas']:
                messagebox.showwarning("Advertencia", "Algunas sucursales no están disponibles")

        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar bases de datos: {str(e)}")
            logger.error(f"Error inicializando BD: {e}")
    
    def abrir_admin(self):
        """Abre la vista de administrador"""
        try:
            admin_window = tk.Toplevel(self.root)
            AdminView(admin_window)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir administración: {str(e)}")
            logger.error(f"Error abriendo admin: {e}")
    
    def abrir_cliente(self):
        """Abre la vista de cliente"""
        try:
            import sys
            import os
            import tempfile
            print("STDOUT: abrir_cliente called", flush=True)
            debug_dir = os.path.join(tempfile.gettempdir(), 'debug_cliente')
            os.makedirs(debug_dir, exist_ok=True)
            with open(os.path.join(debug_dir, 'call.log'), 'w') as f:
                f.write("abrir_cliente called\n")
            
            logger.info("abriendo vista cliente...")
            cliente_window = tk.Toplevel(self.root)
            logger.info("creando ClienteView...")
            ClienteView(cliente_window)
            logger.info("ClienteView creado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir cliente: {str(e)}")
            logger.error(f"Error abriendo cliente: {e}")
    
    def abrir_chatbot(self):
        """Abre la vista del chatbot"""
        try:
            chatbot_window = tk.Toplevel(self.root)
            ChatbotView(chatbot_window)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir chatbot: {str(e)}")
            logger.error(f"Error abriendo chatbot: {e}")
    
    def ver_conexiones(self):
        """Muestra el estado de las conexiones"""
        status = connection_manager.get_status()
        msg = "Estado de Conexiones:\n\n"
        msg += f"MongoDB: {'Conectado' if status['mongodb'] else 'Desconectado'}\n"
        msg += f"SQLite Chiriquí: {'Conectado' if status['chiriqui'] else 'Desconectado'}\n"
        msg += f"SQLite Veraguas: {'Conectado' if status['veraguas'] else 'Desconectado'}"
        messagebox.showinfo("Conexiones", msg)
    
    def forzar_sincronizacion(self):
        """Fuerza la sincronización entre sucursales"""
        try:
            replicacion_service.forzar_sincronizacion()
            messagebox.showinfo("Sincronización", "Sincronización completada con éxito")
        except Exception as e:
            messagebox.showerror("Error", f"Error en sincronización: {str(e)}")
    
    def mostrar_acerca(self):
        """Muestra información de la aplicación"""
        messagebox.showinfo("Acerca de", 
                           "Materiales Ibarra, S.A.\n\n"
                           "Sistema de Gestión Integral\n"
                           "Versión 1.0\n\n"
                           "Desarrollado para la gestión de materiales,\n"
                           "cotizaciones y facturación fiscal.")
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            try:
                replicacion_service.stop()
                connection_manager.close_all()
            except:
                pass
            self.root.destroy()

def main():
    """Función principal"""
    app = AppUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()