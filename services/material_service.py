# -*- coding: utf-8 -*-
"""
Servicio de Materiales - Lógica de Negocio
Materiales Ibarra, S.A.
"""

from typing import List, Optional
from models.material import Material, CategoriaMaterial
from repositories.material_repo import MaterialRepository
from utils.validators import Validators
import logging

logger = logging.getLogger(__name__)

class MaterialService:
    """Servicio para gestión de materiales"""
    
    @staticmethod
    def crear_material(nombre: str, descripcion: str, precio: float, 
                       cantidad: int, categoria: str, unidad: str) -> Optional[Material]:
        """Crea un nuevo material con validación"""
        try:
            if not Validators.validate_not_empty(nombre):
                raise ValueError("El nombre del material no puede estar vacío")
            if not Validators.validate_positive_number(precio):
                raise ValueError("El precio debe ser un número positivo")
            if not Validators.validate_positive_int(cantidad):
                raise ValueError("La cantidad debe ser un número entero positivo")
            
            material = Material(
                nombre=nombre.strip(),
                descripcion=descripcion.strip() if descripcion else "",
                precio=round(float(precio), 2),
                cantidad=int(cantidad),
                categoria=categoria if categoria else CategoriaMaterial.OTROS,
                unidad=unidad if unidad else "UND"
            )
            
            material_id = MaterialRepository.create(material)
            if material_id:
                material.id = material_id
                logger.info(f"Material creado: {material.nombre}")
                return material
            
        except ValueError as ve:
            logger.warning(f"Validación fallida: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error creando material: {e}")
            raise
        
        return None
    
    @staticmethod
    def obtener_todos() -> List[Material]:
        """Obtiene todos los materiales disponibles"""
        logger.info("MaterialService.obtener_todos() called")
        return MaterialRepository.get_all()
    
    @staticmethod
    def obtener_por_id(material_id: int) -> Optional[Material]:
        """Obtiene un material por su ID"""
        return MaterialRepository.get_by_id(material_id)
    
    @staticmethod
    def obtener_por_categoria(categoria: str) -> List[Material]:
        """Obtiene materiales filtrados por categoría"""
        return MaterialRepository.get_by_categoria(categoria)
    
    @staticmethod
    def buscar_materiales(query: str) -> List[Material]:
        """Busca materiales por nombre o descripción"""
        return MaterialRepository.search(query)
    
    @staticmethod
    def actualizar_material(material: Material) -> bool:
        """Actualiza un material existente"""
        try:
            if not Validators.validate_not_empty(material.nombre):
                raise ValueError("El nombre no puede estar vacío")
            if not Validators.validate_positive_number(material.precio):
                raise ValueError("El precio debe ser positivo")
            
            material.precio = round(float(material.precio), 2)
            material.updated_at = __import__('datetime').datetime.now()
            
            return MaterialRepository.update(material)
            
        except ValueError as ve:
            logger.warning(f"Validación fallida: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error actualizando material: {e}")
            return False
    
    @staticmethod
    def eliminar_material(material_id: int) -> bool:
        """Elimina (desactiva) un material"""
        return MaterialRepository.delete(material_id)
    
    @staticmethod
    def get_categorias() -> List[str]:
        """Retorna la lista de categorías disponibles"""
        return CategoriaMaterial.get_all()
    
    @staticmethod
    def validar_disponibilidad(material_id: int, cantidad: int) -> bool:
        """Valida que haya suficiente stock de un material"""
        material = MaterialRepository.get_by_id(material_id)
        if material:
            return material.cantidad >= cantidad
        return False