# -*- coding: utf-8 -*-
"""
Vista de Cliente - Cotizaciones en Tiempo Real
Materiales Ibarra, S.A.
"""

import tkinter as tk
import os
from tkinter import ttk, messagebox, filedialog
from services.material_service import MaterialService
from services.cotizacion_service import CotizacionService
from models.cotizacion import Cotizacion, ItemCotizacion
from utils.validators import Validators
from utils.logger import logger

print("=== cliente_view.py loaded ===")

class ClienteView:
    """Vista del cliente para realizar cotizaciones"""
    
    def __init__(self, parent):
        import sys
        print(f"STDOUT: ClienteView.__init__ called, sys.stdout={sys.stdout}", flush=True)
        import os
        import tempfile
        debug_dir = os.path.join(tempfile.gettempdir(), 'materiales_ibarra_debug')
        os.makedirs(debug_dir, exist_ok=True)
        with open(os.path.join(debug_dir, 'init.log'), 'a') as f:
            f.write("ClienteView.__init__ called\n")
        
        logger.info("=== ClienteView.__init__ start ===")
        self.parent = parent
        self.parent.title("Cliente - Cotizaciones")
        self.parent.geometry("1000x650")
        
        self.materiales_seleccionados = []
        logger.info("Creating widgets...")
        self.create_widgets()
        logger.info("Loading materials...")
        self.cargar_materiales()
        logger.info("=== ClienteView.__init__ done ===")
    
    def create_widgets(self):
        """Crea los widgets de la vista"""
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_cotizacion = ttk.Frame(notebook)
        self.tab_carrito = ttk.Frame(notebook)
        self.tab_historial = ttk.Frame(notebook)
        
        notebook.add(self.tab_cotizacion, text="Nueva Cotización")
        notebook.add(self.tab_carrito, text="Carrito")
        notebook.add(self.tab_historial, text="Historial")
        
        self.crear_tab_cotizacion()
        self.crear_tab_carrito()
        self.crear_tab_historial()
    
    def crear_tab_cotizacion(self):
        """Crea la pestaña de cotización"""
        datos_frame = ttk.LabelFrame(self.tab_cotizacion, text="Datos del Cliente", padding=10)
        datos_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(datos_frame, text="Nombre:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_nombre = ttk.Entry(datos_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, pady=2)
        
        ttk.Label(datos_frame, text="Cédula:").grid(row=0, column=2, sticky='w', padx=10, pady=2)
        self.entry_cedula = ttk.Entry(datos_frame, width=15)
        self.entry_cedula.grid(row=0, column=3, pady=2)
        
        ttk.Label(datos_frame, text="Teléfono:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_telefono = ttk.Entry(datos_frame, width=20)
        self.entry_telefono.grid(row=1, column=1, pady=2)
        
        ttk.Label(datos_frame, text="Email:").grid(row=1, column=2, sticky='w', padx=10, pady=2)
        self.entry_email = ttk.Entry(datos_frame, width=25)
        self.entry_email.grid(row=1, column=3, pady=2)
        
        ttk.Label(datos_frame, text="Sucursal:").grid(row=2, column=0, sticky='w', pady=2)
        self.combo_sucursal = ttk.Combobox(datos_frame, values=["CHIRIQUI", "VERAGUAS", "CHITRE"], width=15)
        self.combo_sucursal.grid(row=2, column=1, pady=2)
        self.combo_sucursal.current(0)
        
        materiales_frame = ttk.LabelFrame(self.tab_cotizacion, text="Catálogo de Materiales", padding=10)
        materiales_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        search_frame = ttk.Frame(materiales_frame)
        search_frame.pack(fill='x', pady=5)
        ttk.Label(search_frame, text="Buscar:").pack(side='left')
        self.entry_buscar = ttk.Entry(search_frame, width=30)
        self.entry_buscar.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_materiales).pack(side='left')
        
        cols = ("ID", "Nombre", "Precio", "Cantidad", "Categoría")
        self.tree_materiales = ttk.Treeview(materiales_frame, columns=cols, show='headings')
        for col in cols:
            self.tree_materiales.heading(col, text=col)
            self.tree_materiales.column(col, width=100)
        self.tree_materiales.pack(fill='both', expand=True)
        
        agregar_frame = ttk.Frame(materiales_frame)
        agregar_frame.pack(fill='x', pady=5)
        
        ttk.Label(agregar_frame, text="Cantidad:").pack(side='left')
        self.entry_cantidad = ttk.Entry(agregar_frame, width=10)
        self.entry_cantidad.pack(side='left', padx=5)
        self.entry_cantidad.insert(0, "1")
        
        ttk.Button(agregar_frame, text="Agregar al Carrito", command=self.agregar_al_carrito).pack(side='left', padx=20)
        
        total_frame = ttk.LabelFrame(self.tab_cotizacion, text="Resumen", padding=10)
        total_frame.pack(fill='x', padx=10, pady=5)
        
        self.lbl_subtotal = ttk.Label(total_frame, text="Subtotal: $0.00", font=('Arial', 12))
        self.lbl_subtotal.pack(side='left', padx=20)
        
        self.lbl_itbms = ttk.Label(total_frame, text="ITBMS (7%): $0.00", font=('Arial', 12))
        self.lbl_itbms.pack(side='left', padx=20)
        
        self.lbl_total = ttk.Label(total_frame, text="TOTAL: $0.00", font=('Arial', 14, 'bold'))
        self.lbl_total.pack(side='left', padx=20)
        
        ttk.Button(total_frame, text="Crear Cotización", command=self.crear_cotizacion).pack(side='right', padx=20)
    
    def crear_tab_carrito(self):
        """Crea la pestaña del carrito"""
        frame = ttk.LabelFrame(self.tab_carrito, text="Carrito de Compras", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        cols = ("Material", "Cantidad", "Precio Unit.", "Subtotal", "Acción")
        self.tree_carrito = ttk.Treeview(frame, columns=cols, show='headings')
        for col in cols:
            self.tree_carrito.heading(col, text=col)
        self.tree_carrito.pack(fill='both', expand=True)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_del_carrito).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar Carrito", command=self.limpiar_carrito).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Generar PDF", command=self.generar_pdf).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Convertir a Factura", command=self.convertir_factura).pack(side='left', padx=5)
    
    def crear_tab_historial(self):
        """Crea la pestaña de historial"""
        frame = ttk.LabelFrame(self.tab_historial, text="Historial de Cotizaciones", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.cargar_historial).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver PDF", command=self.ver_pdf_cotizacion).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Convertir a Factura", command=self.convertir_factura_desde_historial).pack(side='left', padx=5)
        
        cols = ("ID", "Cliente", "Total", "Fecha", "Estado", "PDF")
        self.tree_historial = ttk.Treeview(frame, columns=cols, show='headings')
        for col in cols:
            self.tree_historial.heading(col, text=col)
        self.tree_historial.pack(fill='both', expand=True)
        
        self.cargar_historial()
    
    def cargar_materiales(self):
        """Carga los materiales disponibles"""
        for item in self.tree_materiales.get_children():
            self.tree_materiales.delete(item)
        
        try:
            materiales = MaterialService.obtener_todos()
            logger.info(f"Cargados {len(materiales)} materiales")
            for mat in materiales:
                logger.debug(f"Material: {mat.nombre}, precio: {mat.precio}")
                self.tree_materiales.insert('', tk.END, values=(
                    mat.id, mat.nombre, f"${mat.precio:.2f}", mat.cantidad, mat.categoria
                ))
            if not materiales:
                logger.warning("No se cargaron materiales - lista vacía")
        except Exception as e:
            logger.error(f"Error cargando materiales: {e}")
    
    def buscar_materiales(self):
        """Busca materiales"""
        query = self.entry_buscar.get().strip()
        for item in self.tree_materiales.get_children():
            self.tree_materiales.delete(item)
        
        try:
            if query:
                materiales = MaterialService.buscar_materiales(query)
            else:
                materiales = MaterialService.obtener_todos()
            
            for mat in materiales:
                self.tree_materiales.insert('', tk.END, values=(
                    mat.id, mat.nombre, f"${mat.precio:.2f}", mat.cantidad, mat.categoria
                ))
        except Exception as e:
            logger.error(f"Error buscando materiales: {e}")
    
    def agregar_al_carrito(self):
        """Agrega un material al carrito"""
        selected = self.tree_materiales.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un material")
            return
        
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
            return
        
        item = self.tree_materiales.item(selected[0])
        valores = item['values']
        
        material_id = valores[0]
        nombre = valores[1]
        precio = float(valores[2].replace('$', ''))
        
        subtotal = precio * cantidad
        
        self.materiales_seleccionados.append({
            'material_id': material_id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': subtotal
        })
        
        self.actualizar_carrito()
        messagebox.showinfo("Éxito", f"'{nombre}' agregado al carrito")
    
    def actualizar_carrito(self):
        """Actualiza la vista del carrito"""
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        
        subtotal_total = 0
        for item_data in self.materiales_seleccionados:
            self.tree_carrito.insert('', tk.END, values=(
                item_data['nombre'],
                item_data['cantidad'],
                f"${item_data['precio']:.2f}",
                f"${item_data['subtotal']:.2f}",
                "Eliminar"
            ))
            subtotal_total += item_data['subtotal']
        
        itbms = subtotal_total * 0.07
        total = subtotal_total + itbms
        
        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal_total:.2f}")
        self.lbl_itbms.config(text=f"ITBMS (7%): ${itbms:.2f}")
        self.lbl_total.config(text=f"TOTAL: ${total:.2f}")
    
    def eliminar_del_carrito(self):
        """Elimina un item del carrito"""
        selected = self.tree_carrito.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item para eliminar")
            return
        
        index = self.tree_carrito.index(selected[0])
        del self.materiales_seleccionados[index]
        self.actualizar_carrito()
    
    def limpiar_carrito(self):
        """Limpia el carrito"""
        self.materiales_seleccionados = []
        self.actualizar_carrito()
    
    def crear_cotizacion(self):
        """Crea una nueva cotización"""
        nombre = self.entry_nombre.get().strip()
        if not Validators.validate_not_empty(nombre):
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío")
            return
        
        if not self.materiales_seleccionados:
            messagebox.showerror("Error", "Agregue materiales al carrito")
            return
        
        try:
            cotizacion = CotizacionService.crear_cotizacion(
                cliente_nombre=nombre,
                cliente_cedula=self.entry_cedula.get().strip(),
                cliente_telefono=self.entry_telefono.get().strip(),
                cliente_email=self.entry_email.get().strip(),
                items=self.materiales_seleccionados,
                sucursal=self.combo_sucursal.get()
            )
            
            if cotizacion:
                messagebox.showinfo("Éxito", f"Cotización creada\nTotal: ${cotizacion.total:.2f}")
                self.limpiar_carrito()
                self.cargar_historial()
            else:
                messagebox.showerror("Error", "No se pudo crear la cotización")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            logger.error(f"Error creando cotización: {e}")
    
    def generar_pdf(self):
        """Genera el PDF de la cotización"""
        if not self.materiales_seleccionados:
            messagebox.showwarning("Advertencia", "Carrito vacío")
            return
        
        cotizacion = CotizacionService.crear_cotizacion(
            cliente_nombre=self.entry_nombre.get().strip() or "Cliente",
            cliente_cedula=self.entry_cedula.get().strip(),
            cliente_telefono=self.entry_telefono.get().strip(),
            cliente_email=self.entry_email.get().strip(),
            items=self.materiales_seleccionados,
            sucursal=self.combo_sucursal.get()
        )
        
        if cotizacion:
            ruta_pdf = CotizacionService.generar_pdf(cotizacion.id)
            if ruta_pdf:
                messagebox.showinfo("PDF", f"PDF generado: {ruta_pdf}")
            else:
                messagebox.showerror("Error", "No se pudo generar el PDF")
    
    def convertir_factura(self):
        """Convierte la cotización en factura"""
        if not self.materiales_seleccionados:
            messagebox.showwarning("Advertencia", "Carrito vacío")
            return
        
        messagebox.showinfo("Factura", "Para convertir a factura, primero cree la cotización y luego use la opción en el historial")
    
    def cargar_historial(self):
        """Carga el historial de cotizaciones"""
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)
        
        try:
            cotizaciones = CotizacionService.obtener_todas()
            for cot in cotizaciones:
                self.tree_historial.insert('', tk.END, values=(
                    cot.id, cot.cliente_nombre, f"${cot.total:.2f}",
                    cot.created_at.strftime("%Y-%m-%d %H:%M"), cot.estado, "Sí" if cot.pdf_path else "No"
                ))
        except Exception as e:
            logger.error(f"Error cargando historial: {e}")
    
    def ver_pdf_cotizacion(self):
        """Ver el PDF de una cotización"""
        selected = self.tree_historial.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una cotización")
            return
        
        item = self.tree_historial.item(selected[0])
        valores = item['values']
        cotizacion_id = valores[0]
        
        try:
            cotizacion = CotizacionService.obtener_por_id(cotizacion_id)
            if cotizacion and cotizacion.pdf_path and os.path.exists(cotizacion.pdf_path):
                # Usar subprocess para mayor compatibilidad en Windows
                import subprocess
                try:
                    # Intentar con el visor por defecto de Windows
                    os.startfile(cotizacion.pdf_path)
                except:
                    # Alternativa: usar cmd /start
                    subprocess.Popen(['cmd', '/c', 'start', '', cotizacion.pdf_path])
                messagebox.showinfo("PDF", f"Abriendo: {cotizacion.pdf_path}")
            else:
                # Generar PDF si no existe
                ruta_pdf = CotizacionService.generar_pdf(cotizacion_id)
                if ruta_pdf:
                    messagebox.showinfo("PDF", f"PDF generado: {ruta_pdf}")
                    # Intentar abrir el PDF generado
                    import subprocess
                    try:
                        os.startfile(ruta_pdf)
                    except:
                        subprocess.Popen(['cmd', '/c', 'start', '', ruta_pdf])
                else:
                    messagebox.showwarning("PDF", "No se encontró PDF para esta cotización")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir PDF: {str(e)}")
    
    def convertir_factura_desde_historial(self):
        """Convierte una cotización en factura fiscal"""
        selected = self.tree_historial.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una cotización")
            return
        
        item = self.tree_historial.item(selected[0])
        valores = item['values']
        cotizacion_id = valores[0]
        
        # Pedir datos del cliente para factura
        datos_window = tk.Toplevel(self.parent)
        datos_window.title("Datos para Factura")
        datos_window.geometry("400x250")
        
        ttk.Label(datos_window, text="Cédula/RUC:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        entry_cedula = ttk.Entry(datos_window, width=25)
        entry_cedula.grid(row=0, column=1, pady=5)
        
        ttk.Label(datos_window, text="Dirección:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        entry_direccion = ttk.Entry(datos_window, width=25)
        entry_direccion.grid(row=1, column=1, pady=5)
        
        ttk.Label(datos_window, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        entry_telefono = ttk.Entry(datos_window, width=25)
        entry_telefono.grid(row=2, column=1, pady=5)
        
        def crear_factura():
            try:
                from services.facturacion_service import FacturacionService
                cotizacion = CotizacionService.obtener_por_id(cotizacion_id)
                if cotizacion:
                    ruta_pdf = FacturacionService.crear_factura_desde_cotizacion(
                        cotizacion,
                        entry_cedula.get(),
                        entry_direccion.get(),
                        entry_telefono.get()
                    )
                    if ruta_pdf:
                        messagebox.showinfo("Éxito", f"Factura creada\nPDF: {ruta_pdf}")
                        datos_window.destroy()
                        self.cargar_historial()
                    else:
                        messagebox.showerror("Error", "No se pudo crear la factura")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(datos_window, text="Crear Factura", command=crear_factura).grid(row=3, column=0, columnspan=2, pady=20)