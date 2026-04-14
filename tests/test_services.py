# -*- coding: utf-8 -*-
"""
Script de Pruebas - Materiales Ibarra, S.A.
Verifica el funcionamiento del sistema
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config():
    """Prueba 1: Carga de configuración"""
    print("\n=== PRUEBA 1: Configuración ===")
    try:
        from config.settings import Config, Sucursales
        print("✓ Configuración cargada correctamente")
        print(f"  - MongoDB: {Config.MONGO_URI}")
        print(f"  - Sucursales: {list(Sucursales.__dict__.keys())}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_models():
    """Prueba 2: Modelos de datos"""
    print("\n=== PRUEBA 2: Modelos de Datos ===")
    try:
        from models.material import Material, CategoriaMaterial
        from models.cotizacion import Cotizacion, ItemCotizacion
        from models.factura import Factura
        
        mat = Material(nombre="Cemento", precio=15.50, cantidad=100)
        print(f"✓ Material: {mat.nombre} - ${mat.precio:.2f}")
        
        cot = Cotizacion(cliente_nombre="Juan Perez", sucursal="CHIRIQUI")
        print(f"✓ Cotización: {cot.cliente_nombre} - Sucursal: {cot.sucursal}")
        
        fac = Factura(numero_factura="CH-20240401-ABC123", cliente_nombre="Test")
        print(f"✓ Factura: {fac.numero_factura}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_validators():
    """Prueba 3: Validadores"""
    print("\n=== PRUEBA 3: Validadores ===")
    try:
        from utils.validators import Validators
        
        assert Validators.validate_not_empty("test") == True
        assert Validators.validate_not_empty("") == False
        assert Validators.validate_positive_number(10.5) == True
        assert Validators.validate_positive_number(-5) == False
        assert Validators.validate_decimal_precision(10.5678) == 10.57
        
        print("✓ Validadores funcionando")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_formatters():
    """Prueba 4: Formateadores"""
    print("\n=== PRUEBA 4: Formateadores ===")
    try:
        from utils.formatters import Formatters
        
        assert Formatters.format_currency(1000.50) == "$1,000.50"
        assert Formatters.format_decimal(10.5678, 2) == "10.57"
        
        print("✓ Formateadores funcionando")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_connection_manager():
    """Prueba 5: Gestor de conexiones"""
    print("\n=== PRUEBA 5: Connection Manager ===")
    try:
        from db.connection_manager import connection_manager
        connection_manager.initialize_all()
        status = connection_manager.get_status()
        print(f"✓ Conexiones: MongoDB={status['mongodb']}, Chiriquí={status['chiriqui']}, Veraguas={status['veraguas']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_material_service():
    """Prueba 6: Servicio de materiales"""
    print("\n=== PRUEBA 6: Material Service ===")
    try:
        from services.material_service import MaterialService
        
        materiales = MaterialService.obtener_todos()
        print(f"✓ Materiales en sistema: {len(materiales)}")
        
        categorias = MaterialService.get_categorias()
        print(f"✓ Categorías disponibles: {len(categorias)}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_chatbot():
    """Prueba 7: Chatbot"""
    print("\n=== PRUEBA 7: Chatbot ===")
    try:
        from chatbot.bot import Chatbot
        
        bot = Chatbot()
        respuesta = bot.process_message("hola")
        print(f"✓ Chatbot responde: {respuesta[:50]}...")
        
        respuesta = bot.process_message("estadísticas")
        print(f"✓ Chatbot estadísticas: {respuesta[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_stats():
    """Prueba 8: Estadísticas"""
    print("\n=== PRUEBA 8: Estadísticas ===")
    try:
        from services.stats_service import StatsService
        
        stats = StatsService.get_estadisticas_generales()
        print(f"✓ Total materiales: {stats['total_materiales']}")
        print(f"✓ Total cotizaciones: {stats['total_cotizaciones']}")
        print(f"✓ Total facturas: {stats['total_facturas']}")
        print(f"✓ Ventas totales: ${stats['ventas_totales']:.2f}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_factura_dgi():
    """Prueba 9: Factura DGI"""
    print("\n=== PRUEBA 9: Facturación DGI ===")
    try:
        from models.factura import Factura
        
        fac = Factura(
            cedula_cliente="8-123-456",
            cliente_nombre="Test Cliente",
            cliente_direccion="Calle Principal",
            cliente_telefono="123-4567"
        )
        
        xml = fac.generar_xml_dgi()
        print(f"✓ XML DGI generado, longitud: {len(xml)} caracteres")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_replicacion():
    """Prueba 10: Replicación"""
    print("\n=== PRUEBA 10: Replicación ===")
    try:
        from services.replicacion_service import replicacion_service
        
        replicacion_service.start()
        print("✓ Servicio de replicación iniciado")
        
        replicacion_service.forzar_sincronizacion()
        print("✓ Sincronización forzada completada")
        
        replicacion_service.stop()
        print("✓ Servicio de replicación detenido")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("=" * 50)
    print("PRUEBAS DEL SISTEMA - MATERIALES IBARRA, S.A.")
    print("=" * 50)
    
    tests = [
        test_config,
        test_models,
        test_validators,
        test_formatters,
        test_connection_manager,
        test_material_service,
        test_chatbot,
        test_stats,
        test_factura_dgi,
        test_replicacion
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Excepción en {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"RESULTADO: {passed} pruebas pasadas, {failed} fallidas")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    run_all_tests()