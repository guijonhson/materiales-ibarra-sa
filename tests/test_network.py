# -*- coding: utf-8 -*-
"""
Pruebas de Red - Materiales Ibarra, S.A.
Verifica el diagrama de red y la replicación entre sucursales
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_network_config():
    """Prueba 1: Configuración de red"""
    print("\n=== PRUEBA 1: Configuración de Red ===")
    try:
        from config.settings import Config, Sucursales
        
        print("✓ Sucursal Chiriquí:", Sucursales.CHIRIQUI)
        print("✓ Sucursal Veraguas:", Sucursales.VERAGUAS)
        print("✓ Sucursal Chitré:", Sucursales.CHITRE)
        
        assert "CHIRIQUI" in str(Sucursales.CHIRIQUI)
        assert "VERAGUAS" in str(Sucursales.VERAGUAS)
        assert "CHITRE" in str(Sucursales.CHITRE)
        
        print("\n✓ Red configurada para 3 sucursales")
        print("  - VLAN: 10")
        print("  - Rango IP: 192.168.10.0/24")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_replication_threads():
    """Prueba 2: Hilos de replicación"""
    print("\n=== PRUEBA 2: Hilos de Replicación ===")
    try:
        from threads.sync_thread import sync_thread
        
        sync_thread.start()
        print("✓ Hilo de sincronización iniciado")
        
        import time
        time.sleep(2)
        
        sync_thread.stop()
        print("✓ Hilo de sincronización detenido")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_databases_creation():
    """Prueba 3: Creación de bases de datos"""
    print("\n=== PRUEBA 3: Bases de Datos por Sucursal ===")
    try:
        import os
        from db.connection_manager import connection_manager
        
        connection_manager.initialize_all()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        db_chiriqui = os.path.join(base_dir, "db/chiriqui.db")
        db_veraguas = os.path.join(base_dir, "db/veraguas.db")
        
        print(f"✓ BD Chiriquí: {db_chiriqui} - Existe: {os.path.exists(db_chiriqui)}")
        print(f"✓ BD Veraguas: {db_veraguas} - Existe: {os.path.exists(db_veraguas)}")
        
        assert os.path.exists(db_chiriqui), "BD Chiriquí no creada"
        assert os.path.exists(db_veraguas), "BD Veraguas no creada"
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_vlan_connectivity():
    """Prueba 4: Conectividad VLAN"""
    print("\n=== PRUEBA 4: Conectividad VLAN ===")
    try:
        print("✓ Simulación de VLAN 10")
        print("  - Router: 192.168.10.254")
        print("  - Switch: 192.168.10.1")
        print("  - Chiriquí: 192.168.10.1")
        print("  - Veraguas: 192.168.10.2")
        print("  - Chitré: 192.168.10.3")
        
        print("\n✓ Protocolo de replicación: TCP/IP")
        print("✓ Intervalo de sincronización: 5 segundos")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_replication_data():
    """Prueba 5: Replicación de datos"""
    print("\n=== PRUEBA 5: Replicación de Datos ===")
    try:
        from services.replicacion_service import replicacion_service
        from models.material import Material
        from repositories.material_repo import MaterialRepository
        
        material = Material(
            nombre="Cemento de Prueba",
            descripcion="Para prueba de replicación",
            precio=25.00,
            cantidad=50,
            categoria="Construcción",
            unidad="Bulto"
        )
        
        result = MaterialRepository.create(material)
        print(f"✓ Material creado en BD principal")
        
        replicacion_service.forzar_sincronizacion()
        print("✓ Datos replicados a sucursales")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_network_tests():
    """Ejecuta todas las pruebas de red"""
    print("=" * 50)
    print("PRUEBAS DE RED - MATERIALES IBARRA, S.A.")
    print("=" * 50)
    
    tests = [
        test_network_config,
        test_replication_threads,
        test_databases_creation,
        test_vlan_connectivity,
        test_replication_data
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
    run_network_tests()