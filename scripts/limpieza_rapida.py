#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/limpieza_rapida.py
Limpieza RAPIDA de todas las bases de datos (MongoDB + SQLite)
Ejecutar para resetear completamente el sistema
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def limpiar_mongodb():
    """Limpia MongoDB"""
    print("\n[1/4] Limpiando MongoDB...")
    
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        bases = ["materiales_ibarra", "chitre_db", "materiales", "cotizaciones_db"]
        for base in bases:
            try:
                client.drop_database(base)
                print(f"  [X] Eliminada: {base}")
            except Exception as e:
                print(f"  - No existe: {base}")
        
        client.close()
        print("  MongoDB limpiado")
        return True
    except ImportError:
        print("  [!] pymongo no instalado")
        return False
    except Exception as e:
        print(f"  [!] Error: {e}")
        return False


def limpiar_sqlite():
    """Limpia archivos SQLite"""
    print("\n[2/4] Limpiando SQLite...")
    
    db_files = [
        PROJECT_ROOT / "db" / "chiriqui.db",
        PROJECT_ROOT / "db" / "veraguas.db",
        PROJECT_ROOT / "db" / "chitre.db",
        PROJECT_ROOT / "chiriqui.db",
    ]
    
    for db in db_files:
        if db.exists():
            try:
                db.unlink()
                print(f"  [X] Eliminado: {db.name}")
            except Exception as e:
                print(f"  [!] Error: {db.name} - {e}")
    
    print("  SQLite limpiado")
    return True


def limpiar_pdfs_y_logs():
    """Limpia PDFs y logs"""
    print("\n[3/4] Limpiando PDFs y logs...")
    
    folders_to_clean = [
        PROJECT_ROOT / "storage" / "facturas",
        PROJECT_ROOT / "logs",
    ]
    
    for folder in folders_to_clean:
        if folder.exists():
            count = 0
            for item in folder.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                    count += 1
                except:
                    pass
            print(f"  [X] Limpiada: {folder.name}/ ({count} elementos)")
        else:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"  [X] Creada (vacia): {folder.name}/")
    
    return True


def limpiar_temporales():
    """Limpia archivos temporales de Python"""
    print("\n[4/4] Limpiando archivos temporales...")
    
    pycache = list(PROJECT_ROOT.rglob("__pycache__"))
    pyc = list(PROJECT_ROOT.rglob("*.pyc"))
    
    for carpeta in pycache:
        try:
            if "venv" not in str(carpeta):
                shutil.rmtree(carpeta)
        except:
            pass
    
    for archivo in pyc:
        try:
            archivo.unlink()
        except:
            pass
    
    print(f"  [X] __pycache__ eliminados: {len(pycache)}")
    print(f"  [X] .pyc eliminados: {len(pyc)}")
    return True


def main():
    force = "--force" in sys.argv or "-f" in sys.argv
    
    print("=" * 60)
    print("LIMPIEZA RAPIDA - Materiales Ibarra, S.A.")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    print("\nEsto ELIMINARA:")
    print("  - MongoDB: materiales_ibarra")
    print("  - SQLite: chiriqui.db, veraguas.db, chitre.db")
    print("  - Todos los PDFs en storage/facturas/")
    print("  - Todos los logs en logs/")
    print("  - Archivos __pycache__ y *.pyc")
    print("\nEl CODIGO del sistema se CONSERVA intacto")
    
    if not force:
        respuesta = input("\nContinuar? (escriba 'LIMPIAR TODO' para confirmar): ")
        
        if respuesta != "LIMPIAR TODO":
            print("\nOperacion cancelada.")
            sys.exit(0)
    
    print("\n" + "=" * 60)
    print("EJECUTANDO LIMPIEZA...")
    print("=" * 60)
    
    limpiar_mongodb()
    limpiar_sqlite()
    limpiar_pdfs_y_logs()
    limpiar_temporales()
    
    print("\n" + "=" * 60)
    print("LIMPIEZA COMPLETADA")
    print("=" * 60)
    print("\nEl sistema esta limpio. Ejecute 'python iniciar.pyw' para iniciar.")


if __name__ == "__main__":
    main()
