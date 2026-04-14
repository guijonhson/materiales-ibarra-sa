# -*- coding: utf-8 -*-
"""
Vista de Administrador - Gestión de Materiales e Inventario
Materiales Ibarra, S.A.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from services.material_service import MaterialService
from services.cotizacion_service import CotizacionService
from services.facturacion_service import FacturacionService
from services.stats_service import StatsService
from models.material import CategoriaMaterial
from utils.formatters import Formatters
from utils.validators import Validators
from utils.logger import logger

class AdminView:
    """Vista del administrador"""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Administración - Materiales Ibarra")
        self.parent.geometry("900x600")
        
        self.create_widgets()
        self.cargar_materiales()
    
    def create_widgets(self):
        """Crea los widgets de la vista"""
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_materiales = ttk.Frame(notebook)
        self.tab_inventario = ttk.Frame(notebook)
        self.tab_facturas = ttk.Frame(notebook)
        self.tab_estadisticas = ttk.Frame(notebook)
        
        notebook.add(self.tab_materiales, text="Gestión de Materiales")
        notebook.add(self.tab_inventario, text="Inventario")
        notebook.add(self.tab_facturas, text="Facturación")
        notebook.add(self.tab_estadisticas, text="Estadísticas")
        
        self.crear_tab_materiales()
        self.crear_tab_inventario()
        self.crear_tab_facturas()
        self.crear_tab_estadisticas()
    
    def crear_tab_materiales(self):
        """Crea la pestaña de materiales"""
        frame = ttk.LabelFrame(self.tab_materiales, text="Nuevo Material", padding=10)
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_nombre = ttk.Entry(frame, width=30)
        self.entry_nombre.grid(row=0, column=1, pady=2)
        
        ttk.Label(frame, text="Descripción:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_descripcion = ttk.Entry(frame, width=30)
        self.entry_descripcion.grid(row=1, column=1, pady=2)
        
        ttk.Label(frame, text="Precio:").grid(row=2, column=0, sticky='w', pady=2)
        self.entry_precio = ttk.Entry(frame, width=15)
        self.entry_precio.grid(row=2, column=1, sticky='w', pady=2)
        
        ttk.Label(frame, text="Cantidad:").grid(row=3, column=0, sticky='w', pady=2)
        self.entry_cantidad = ttk.Entry(frame, width=15)
        self.entry_cantidad.grid(row=3, column=1, sticky='w', pady=2)
        
        ttk.Label(frame, text="Categoría:").grid(row=4, column=0, sticky='w', pady=2)
        self.combo_categoria = ttk.Combobox(frame, values=MaterialService.get_categorias(), width=27)
        self.combo_categoria.grid(row=4, column=1, pady=2)
        self.combo_categoria.current(0)
        
        ttk.Label(frame, text="Unidad:").grid(row=5, column=0, sticky='w', pady=2)
        self.entry_unidad = ttk.Entry(frame, width=15)
        self.entry_unidad.grid(row=5, column=1, sticky='w', pady=2)
        self.entry_unidad.insert(0, "UND")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Agregar Material", command=self.agregar_material).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).pack(side='left', padx=5)
        
        list_frame = ttk.LabelFrame(self.tab_materiales, text="Lista de Materiales", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        cols = ("ID", "Nombre", "Precio", "Cantidad", "Categoría", "Unidad")
        self.tree_materiales = ttk.Treeview(list_frame, columns=cols, show='headings')
        for col in cols:
            self.tree_materiales.heading(col, text=col)
            self.tree_materiales.column(col, width=100)
        self.tree_materiales.pack(fill='both', expand=True)
        
        btn_action_frame = ttk.Frame(list_frame)
        btn_action_frame.pack(pady=5)
        ttk.Button(btn_action_frame, text="Editar", command=self.editar_material).pack(side='left', padx=5)
        ttk.Button(btn_action_frame, text="Eliminar", command=self.eliminar_material).pack(side='left', padx=5)
    
    def crear_tab_inventario(self):
        """Crea la pestaña de inventario"""
        frame = ttk.LabelFrame(self.tab_inventario, text="Inventario por Sucursal", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        sucursal_frame = ttk.Frame(frame)
        sucursal_frame.pack(fill='x', pady=5)
        ttk.Label(sucursal_frame, text="Sucursal:").pack(side='left', padx=5)
        self.combo_sucursal_inv = ttk.Combobox(sucursal_frame, values=["CHIRIQUI", "VERAGUAS", "CHITRE"], width=15)
        self.combo_sucursal_inv.pack(side='left', padx=5)
        self.combo_sucursal_inv.current(0)
        ttk.Button(sucursal_frame, text="Ver Inventario", command=self.cargar_inventario).pack(side='left', padx=5)
        
        cols = ("Nombre", "Categoría", "Cantidad", "Precio Unit.", "Valor Total")
        self.tree_inventario = ttk.Treeview(frame, columns=cols, show='headings')
        for col in cols:
            self.tree_inventario.heading(col, text=col)
        self.tree_inventario.pack(fill='both', expand=True)
        
        total_frame = ttk.Frame(frame)
        total_frame.pack(fill='x', pady=5)
        self.lbl_total_inventario = ttk.Label(total_frame, text="Total Inventario: $0.00", font=('Arial', 12, 'bold'))
        self.lbl_total_inventario.pack(side='left', padx=10)
        
        self.cargar_inventario()
    
    def crear_tab_facturas(self):
        """Crea la pestaña de facturas"""
        frame = ttk.LabelFrame(self.tab_facturas, text="Facturas Fiscales", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.cargar_facturas).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver PDF", command=self.ver_pdf_factura).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver XML DGI", command=self.ver_xml_dgi).pack(side='left', padx=5)
        
        cols = ("No. Factura", "Cliente", "Cédula", "Total", "Fecha", "Sucursal")
        self.tree_facturas = ttk.Treeview(frame, columns=cols, show='headings')
        for col in cols:
            self.tree_facturas.heading(col, text=col)
        self.tree_facturas.pack(fill='both', expand=True)
        
        self.cargar_facturas()
    
    def crear_tab_estadisticas(self):
        """Crea la pestaña de estadísticas"""
        frame = ttk.LabelFrame(self.tab_estadisticas, text="Estadísticas del Sistema", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = tk.Text(frame, height=20, width=80, font=('Courier', 10))
        self.stats_text.pack(fill='both', expand=True)
        
        ttk.Button(frame, text="Actualizar Estadísticas", command=self.cargar_estadisticas).pack(pady=10)
    
    def agregar_material(self):
        """Agrega un nuevo material"""
        try:
            nombre = self.entry_nombre.get().strip()
            if not Validators.validate_not_empty(nombre):
                messagebox.showerror("Error", "El nombre del material no puede estar vacío")
                return
            
            try:
                precio = float(self.entry_precio.get())
                cantidad = int(self.entry_cantidad.get())
                # Error Alto admin_view.py L136-173: Validar números negativos
                if precio < 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo")
                    return
                if cantidad < 0:
                    messagebox.showerror("Error", "La cantidad no puede ser negativa")
                    return
                if precio <= 0 or cantidad <= 0:
                    messagebox.showerror("Error", "Precio y cantidad deben ser positivos")
                    return
            except ValueError:
                messagebox.showerror("Error", "Precio y cantidad deben ser números válidos")
                return
            
            material = MaterialService.crear_material(
                nombre=nombre,
                descripcion=self.entry_descripcion.get().strip(),
                precio=precio,
                cantidad=cantidad,
                categoria=self.combo_categoria.get(),
                unidad=self.entry_unidad.get().strip()
            )
            
            if material:
                messagebox.showinfo("Éxito", f"Material '{nombre}' agregado correctamente")
                self.limpiar_formulario()
                self.cargar_materiales()
                logger.info(f"Material agregado: {nombre}")
            else:
                messagebox.showerror("Error", "No se pudo agregar el material")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar material: {str(e)}")
            logger.error(f"Error agregando material: {e}")
    
    def limpiar_formulario(self):
        """Limpia el formulario de materiales"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_unidad.delete(0, tk.END)
        self.entry_unidad.insert(0, "UND")
        self.combo_categoria.current(0)
    
    def cargar_materiales(self):
        """Carga los materiales en el treeview"""
        for item in self.tree_materiales.get_children():
            self.tree_materiales.delete(item)
        
        try:
            materiales = MaterialService.obtener_todos()
            for mat in materiales:
                self.tree_materiales.insert('', tk.END, values=(
                    mat.id, mat.nombre, f"${mat.precio:.2f}", mat.cantidad,
                    mat.categoria, mat.unidad
                ))
        except Exception as e:
            logger.error(f"Error cargando materiales: {e}")
    
    def editar_material(self):
        """Edita un material seleccionado"""
        selected = self.tree_materiales.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un material para editar")
            return
        
        item = self.tree_materiales.item(selected[0])
        valores = item['values']
        
        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Editar Material")
        edit_window.geometry("400x350")
        
        ttk.Label(edit_window, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        entry_nombre = ttk.Entry(edit_window, width=30)
        entry_nombre.grid(row=0, column=1, pady=5)
        entry_nombre.insert(0, valores[1])
        
        ttk.Label(edit_window, text="Precio:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        entry_precio = ttk.Entry(edit_window, width=15)
        entry_precio.grid(row=1, column=1, pady=5, sticky='w')
        entry_precio.insert(0, valores[2].replace('$', ''))
        
        ttk.Label(edit_window, text="Cantidad:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        entry_cantidad = ttk.Entry(edit_window, width=15)
        entry_cantidad.grid(row=2, column=1, pady=5, sticky='w')
        entry_cantidad.insert(0, valores[3])
        
        def guardar_cambios():
            try:
                from models.material import Material
                material = Material(
                    id=valores[0],
                    nombre=entry_nombre.get(),
                    precio=float(entry_precio.get()),
                    cantidad=int(entry_cantidad.get())
                )
                if MaterialService.actualizar_material(material):
                    messagebox.showinfo("Éxito", "Material actualizado")
                    edit_window.destroy()
                    self.cargar_materiales()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(edit_window, text="Guardar", command=guardar_cambios).grid(row=3, column=0, columnspan=2, pady=20)
    
    def eliminar_material(self):
        """Elimina un material seleccionado"""
        selected = self.tree_materiales.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un material para eliminar")
            return
        
        item = self.tree_materiales.item(selected[0])
        valores = item['values']
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el material '{valores[1]}'?"):
            try:
                if MaterialService.eliminar_material(valores[0]):
                    messagebox.showinfo("Éxito", "Material eliminado")
                    self.cargar_materiales()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_inventario(self):
        """Carga el inventario de la sucursal seleccionada"""
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        
        try:
            sucursal = self.combo_sucursal_inv.get()
            materiales = MaterialService.obtener_todos()
            
            total_inventario = 0
            for mat in materiales:
                valor_total = mat.precio * mat.cantidad
                total_inventario += valor_total
                self.tree_inventario.insert('', tk.END, values=(
                    mat.nombre, mat.categoria, mat.cantidad,
                    f"${mat.precio:.2f}", f"${valor_total:.2f}"
                ))
            
            self.lbl_total_inventario.config(text=f"Total Inventario ({sucursal}): ${total_inventario:.2f}")
        except Exception as e:
            logger.error(f"Error cargando inventario: {e}")
    
    def cargar_facturas(self):
        """Carga las facturas en el treeview"""
        for item in self.tree_facturas.get_children():
            self.tree_facturas.delete(item)
        
        try:
            from services.facturacion_service import FacturacionService
            facturas = FacturacionService.obtener_todas()
            
            for fac in facturas:
                fecha = fac.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(fac.created_at, 'strftime') else str(fac.created_at)
                self.tree_facturas.insert('', tk.END, values=(
                    fac.numero_factura, fac.cliente_nombre, fac.cedula_cliente,
                    f"${fac.total:.2f}", fecha, fac.sucursal
                ))
        except Exception as e:
            logger.error(f"Error cargando facturas: {e}")
    
    def ver_pdf_factura(self):
        """Ver el PDF de una factura"""
        selected = self.tree_facturas.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una factura")
            return
        
        item = self.tree_facturas.item(selected[0])
        valores = item['values']
        numero_factura = valores[0]
        
        try:
            import os
            from services.facturacion_service import FacturacionService
            from config.settings import Config
            
            pdf_encontrado = None
            for root, dirs, files in os.walk(Config.FACTURAS_DIR):
                for f in files:
                    if numero_factura in f and f.endswith('.pdf'):
                        pdf_encontrado = os.path.join(root, f)
                        break
                if pdf_encontrado:
                    break
            
            if pdf_encontrado:
                try:
                    os.startfile(pdf_encontrado)
                except:
                    import subprocess
                    subprocess.Popen(['cmd', '/c', 'start', '', pdf_encontrado])
                messagebox.showinfo("PDF", f"Abriendo: {pdf_encontrado}")
            else:
                messagebox.showwarning("PDF", f"No se encontró:\n{numero_factura}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def cargar_estadisticas(self):
        """Carga las estadísticas"""
        try:
            stats = StatsService.get_estadisticas_generales()
            self.stats_text.delete('1.0', tk.END)
            self.stats_text.insert('1.0', f"""=== ESTADÍSTICAS DEL SISTEMA ===
            
Total Materiales: {stats['total_materiales']}
Total Cotizaciones: {stats['total_cotizaciones']}
Total Facturas: {stats['total_facturas']}
Ventas Totales: ${stats['ventas_totales']:.2f}

=== MATERIALES POR CATEGORÍA ===
""")
            for cat, cant in stats['materiales_por_categoria'].items():
                self.stats_text.insert(tk.END, f"  {cat}: {cant}\n")
            
            self.stats_text.insert(tk.END, "\n=== COTIZACIONES POR SUCURSAL ===\n")
            for suc, cant in stats['cotizaciones_por_sucursal'].items():
                self.stats_text.insert(tk.END, f"  {suc}: {cant}\n")
                
        except Exception as e:
            logger.error(f"Error cargando estadísticas: {e}")
    
    def ver_xml_dgi(self):
        """Muestra el XML de una factura DGI"""
        selected = self.tree_facturas.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una factura")
            return
        
        messagebox.showinfo("XML DGI", "Funcionalidad de visualización de XML DGI")