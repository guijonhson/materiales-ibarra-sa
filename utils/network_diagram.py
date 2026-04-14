# -*- coding: utf-8 -*-
"""
Diagrama de Red LAN - Sucursales Materiales Ibarra, S.A.
Topología: VLAN para conectar las 3 sucursales
"""

import tkinter as tk
from tkinter import ttk

class NetworkDiagram:
    """Diagrama de Red LAN entre sucursales"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Diagrama de Red - Materiales Ibarra, S.A.")
        self.root.geometry("900x600")
        self.create_diagram()
    
    def create_diagram(self):
        """Crea el diagrama de red"""
        canvas = tk.Canvas(self.root, bg="white", width=900, height=550)
        canvas.pack(padx=10, pady=10)
        
        canvas.create_text(450, 30, text="DIAGRAMA DE RED LAN - SUCURSALES MATERIALES IBARRA, S.A.", 
                          font=("Arial", 14, "bold"), fill="#2C3E50")
        
        canvas.create_text(450, 55, text="Topología: VLAN 10 (192.168.10.0/24)", 
                          font=("Arial", 10), fill="#7f8c8d")
        
        # Router principal
        self.draw_router(canvas, 450, 120)
        
        # Switch central
        self.draw_switch(canvas, 450, 200)
        
        # Sucursales
        self.draw_branch(canvas, 150, 350, "CHIRIQUÍ\n(Vía Panamericana)\n192.168.10.1", "#3498db")
        self.draw_branch(canvas, 450, 350, "VERAGUAS\n(Frente Mall Santiago)\n192.168.10.2", "#27ae60")
        self.draw_branch(canvas, 750, 350, "CHITRÉ\n(Frente Hotel Gran Azuero)\n192.168.10.3", "#e74c3c")
        
        # Conexiones
        self.draw_connection(canvas, 450, 155, 450, 180)
        self.draw_connection(canvas, 350, 200, 150, 280)
        self.draw_connection(canvas, 450, 220, 450, 280)
        self.draw_connection(canvas, 550, 200, 750, 280)
        
        # Leyenda
        self.draw_legend(canvas)
        
        # Servidor MongoDB (simulado en la nube)
        self.draw_server(canvas, 450, 480, "MongoDB\n(Principal)", "#9b59b6")
        
        self.draw_connection(canvas, 450, 380, 450, 450)
        
        # Info de replicación
        info_frame = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=5)
        info_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(info_frame, text="📡 Replicación en tiempo real: Intervalo de 5 segundos | Protocolo: TCP/IP | VLAN: 10", 
                bg="#ecf0f1", font=("Arial", 9)).pack()
    
    def draw_router(self, canvas, x, y):
        """Dibuja un router"""
        canvas.create_rectangle(x-30, y-15, x+30, y+15, fill="#2c3e50", outline="#2c3e50")
        canvas.create_text(x, y, text="ROUTER", fill="white", font=("Arial", 8, "bold"))
        canvas.create_arc(x-25, y-25, x+25, y+25, start=0, extent=180, fill="#2c3e50", outline="#2c3e50")
    
    def draw_switch(self, canvas, x, y):
        """Dibuja un switch"""
        canvas.create_rectangle(x-40, y-20, x+40, y+20, fill="#34495e", outline="#34495e")
        canvas.create_text(x, y, text="SWITCH VLAN 10", fill="white", font=("Arial", 8, "bold"))
        canvas.create_arc(x-35, y-25, x+35, y+25, start=0, extent=180, fill="#34495e", outline="#34495e")
    
    def draw_branch(self, canvas, x, y, label, color):
        """Dibuja una sucursal"""
        canvas.create_oval(x-60, y-40, x+60, y+40, fill=color, outline=color)
        canvas.create_text(x, y, text=label, fill="white", font=("Arial", 9, "bold"), justify="center")
        
        # Base de datos icono
        canvas.create_rectangle(x-15, y+50, x+15, y+70, fill="#95a5a6", outline="#95a5a6")
        canvas.create_text(x, y+60, text="SQLite", fill="white", font=("Arial", 7))
        
        # IP
        canvas.create_text(x, y+85, text=f"Gateway: {label.split()[2]}", fill="#2c3e50", font=("Arial", 8))
    
    def draw_server(self, canvas, x, y, label, color):
        """Dibuja un servidor"""
        canvas.create_rectangle(x-40, y-25, x+40, y+25, fill=color, outline=color)
        canvas.create_text(x, y, text=label, fill="white", font=("Arial", 9, "bold"), justify="center")
    
    def draw_connection(self, canvas, x1, y1, x2, y2):
        """Dibuja una conexión"""
        canvas.create_line(x1, y1, x2, y2, fill="#7f8c8d", width=2)
    
    def draw_legend(self, canvas):
        """Dibuja la leyenda"""
        canvas.create_rectangle(50, 420, 250, 510, fill="#f8f9fa", outline="#bdc3c7")
        canvas.create_text(150, 435, text="LEYENDA", font=("Arial", 10, "bold"), fill="#2c3e50")
        
        canvas.create_oval(70, 455, 90, 475, fill="#3498db", outline="#3498db")
        canvas.create_text(150, 465, text="Sucursal", fill="#2c3e50", font=("Arial", 9))
        
        canvas.create_rectangle(70, 485, 90, 495, fill="#95a5a6", outline="#95a5a6")
        canvas.create_text(150, 490, text="Base de Datos Local", fill="#2c3e50", font=("Arial", 9))

if __name__ == "__main__":
    app = NetworkDiagram()
    app.root.mainloop()