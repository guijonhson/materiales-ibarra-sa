#!/usr/bin/env python3
"""
Health check para el servicio de réplicas en Docker
"""

import os
import sys
import sqlite3
from pathlib import Path

DATA_DIR = Path("/data")
MONGO_HOST = os.getenv("MONGO_HOST", "host.docker.internal")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MODO = os.getenv("MODO", "central")
SUCURSAL = os.getenv("SUCURSAL", "chiriqui")


def check_mongodb():
    try:
        from pymongo import MongoClient
        client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        client.close()
        print(f"MongoDB en {MONGO_HOST}:{MONGO_PORT} - Conectado")
        return True
    except Exception as e:
        print(f"MongoDB error: {e}")
        return False


def check_sqlite():
    sucursales = ["chiriqui", "veraguas", "chitre"] if MODO == "central" else [SUCURSAL]
    all_ok = True
    for suc in sucursales:
        db_path = DATA_DIR / suc / f"{suc}.db"
        if not db_path.exists():
            print(f"{suc}.db - No existe")
            all_ok = False
            continue
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM materiales")
            count = cursor.fetchone()[0]
            print(f"{suc}.db - {count} materiales")
            conn.close()
        except Exception as e:
            print(f"{suc}.db - Error: {e}")
            all_ok = False
    return all_ok


if __name__ == "__main__":
    print("=" * 50)
    print("HEALTH CHECK - Servicio de Replicas Docker")
    print("=" * 50)
    mongo_ok = check_mongodb()
    sqlite_ok = check_sqlite()
    print("=" * 50)
    sys.exit(0 if (mongo_ok and sqlite_ok) else 1)