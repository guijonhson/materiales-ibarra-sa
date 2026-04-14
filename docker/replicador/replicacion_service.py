#!/usr/bin/env python3
"""
Servicio de réplicas para Docker - Consulta MongoDB (Windows) y actualiza SQLite
Respetando AGENTS.md: MongoDB es la base principal en Windows
"""

import os
import sys
import json
import time
import sqlite3
import signal
import logging
import threading
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
except ImportError:
    print("Error: pymongo no instalado")
    sys.exit(1)

# ============================================================
# CONFIGURACIÓN
# ============================================================
MONGO_HOST = os.getenv("MONGO_HOST", "host.docker.internal")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DB = os.getenv("MONGO_DB", "materiales_ibarra")
REPLICACION_INTERVALO = int(os.getenv("REPLICACION_INTERVALO", "5"))
MODO = os.getenv("MODO", "central")
SUCURSAL = os.getenv("SUCURSAL", "chiriqui")

DATA_DIR = Path("/data")
CHIRIQUI_DIR = DATA_DIR / "chiriqui"
VERAGUAS_DIR = DATA_DIR / "veraguas"
CHITRE_DIR = DATA_DIR / "chitre"

for d in [CHIRIQUI_DIR, VERAGUAS_DIR, CHITRE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

# ============================================================
# LOGGING
# ============================================================
LOG_DIR = Path("/var/log/replicacion")
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / "replicacion.log"
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console)

# ============================================================
# ESQUEMA SQLITE
# ============================================================
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS materiales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mongo_id TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL UNIQUE,
    costo REAL NOT NULL CHECK(costo >= 0),
    cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
    descripcion TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_materiales_nombre ON materiales(nombre);
CREATE INDEX IF NOT EXISTS idx_materiales_mongo_id ON materiales(mongo_id);

CREATE TABLE IF NOT EXISTS cotizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    folio TEXT UNIQUE NOT NULL,
    cliente_nombre TEXT NOT NULL,
    cliente_ruc TEXT,
    fecha TEXT NOT NULL,
    items TEXT NOT NULL,
    subtotal REAL NOT NULL,
    itbms REAL NOT NULL,
    total REAL NOT NULL,
    pdf_path TEXT,
    created_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_cotizaciones_folio ON cotizaciones(folio);
CREATE INDEX IF NOT EXISTS idx_cotizaciones_fecha ON cotizaciones(fecha);
"""


def init_database(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    logger.info(f"Base inicializada: {db_path.name}")


def get_db_path(sucursal: str) -> Path:
    if sucursal == "chiriqui":
        return CHIRIQUI_DIR / "chiriqui.db"
    elif sucursal == "veraguas":
        return VERAGUAS_DIR / "veraguas.db"
    elif sucursal == "chitre":
        return CHITRE_DIR / "chitre.db"
    raise ValueError(f"Sucursal desconocida: {sucursal}")


def ensure_database(sucursal: str):
    db_path = get_db_path(sucursal)
    if not db_path.exists():
        init_database(db_path)
        logger.info(f"Creada base para {sucursal}")
    else:
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='materiales'")
            if not cursor.fetchone():
                cursor.executescript(SCHEMA_SQL)
                conn.commit()
                logger.info(f"Tablas recreadas en {sucursal}")
            conn.close()
        except Exception as e:
            logger.error(f"Error verificando {sucursal}: {e}")
            init_database(db_path)


class MongoDBClient:
    def __init__(self):
        self.client = None
        self.db = None
        self._conectar()

    def _conectar(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[MONGO_DB]
            logger.info(f"Conectado a MongoDB en Windows: {MONGO_HOST}:{MONGO_PORT}")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"No se pudo conectar a MongoDB: {e}")
            self.client = None
            return False

    def is_connected(self):
        if not self.client:
            return self._conectar()
        try:
            self.client.admin.command('ping')
            return True
        except:
            return self._conectar()

    def get_materiales(self):
        if not self.is_connected():
            return []
        try:
            return list(self.db.materiales.find())
        except Exception as e:
            logger.error(f"Error obteniendo materiales: {e}")
            return []

    def get_cotizaciones(self, limite=100):
        if not self.is_connected():
            return []
        try:
            return list(self.db.cotizaciones.find().sort("fecha", -1).limit(limite))
        except Exception as e:
            logger.error(f"Error obteniendo cotizaciones: {e}")
            return []


class ReplicacionService:
    def __init__(self, modo="central", sucursal="chiriqui"):
        self.modo = modo
        self.sucursal = sucursal
        self.mongo = MongoDBClient()
        self.running = False
        self.thread = None

    def get_sucursales(self):
        if self.modo == "central":
            return ["chiriqui", "veraguas", "chitre"]
        return [self.sucursal]

    def replicar_materiales(self, sucursal: str) -> int:
        materiales = self.mongo.get_materiales()
        if not materiales:
            return 0

        db_path = get_db_path(sucursal)
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        count = 0
        for material in materiales:
            if not material.get('nombre'):
                continue
            precio = material.get("costo") or material.get("precio") or 0
            cursor.execute("""
                INSERT OR REPLACE INTO materiales 
                (mongo_id, nombre, costo, cantidad, descripcion, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(material.get('_id')),
                material.get('nombre'),
                precio,
                material.get('cantidad', 0),
                material.get('descripcion', ''),
                material.get('updated_at', datetime.now().isoformat())
            ))
            count += 1

        conn.commit()
        conn.close()
        return count

    def replicar_cotizaciones(self, sucursal: str) -> int:
        cotizaciones = self.mongo.get_cotizaciones()
        if not cotizaciones:
            return 0

        db_path = get_db_path(sucursal)
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        count = 0
        for cotizacion in cotizaciones:
            if not cotizacion.get('id'):
                continue
            cursor.execute("""
                INSERT OR REPLACE INTO cotizaciones 
                (folio, cliente_nombre, cliente_ruc, fecha, items, subtotal, itbms, total, pdf_path, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(cotizacion.get('id')),
                cotizacion.get('cliente_nombre', ''),
                cotizacion.get('cliente_cedula', ''),
                cotizacion.get('created_at', datetime.now().isoformat()),
                json.dumps(cotizacion.get('items', [])),
                cotizacion.get('subtotal', 0),
                cotizacion.get('itbms', 0),
                cotizacion.get('total', 0),
                cotizacion.get('pdf_path', ''),
                cotizacion.get('created_at', datetime.now().isoformat())
            ))
            count += 1

        conn.commit()
        conn.close()
        return count

    def replicar_todo(self):
        sucursales = self.get_sucursales()
        for sucursal in sucursales:
            try:
                ensure_database(sucursal)
                mat_count = self.replicar_materiales(sucursal)
                cot_count = self.replicar_cotizaciones(sucursal)
                if mat_count > 0 or cot_count > 0:
                    logger.info(f"[OK] {sucursal}: {mat_count} materiales, {cot_count} cotizaciones")
            except Exception as e:
                logger.error(f"Error replicando {sucursal}: {e}")

    def _loop(self):
        logger.info("=" * 60)
        logger.info("INICIANDO SERVICIO DE REPLICAS (DOCKER)")
        logger.info(f"Modo: {self.modo}")
        logger.info(f"MongoDB: {MONGO_HOST}:{MONGO_PORT}")
        logger.info(f"Intervalo: {REPLICACION_INTERVALO}s")
        logger.info("=" * 60)

        while self.running:
            try:
                start = time.time()
                self.replicar_todo()
                elapsed = time.time() - start
                if elapsed > REPLICACION_INTERVALO:
                    logger.warning(f"Replicacion tardo {elapsed:.2f}s")
                time.sleep(max(0, REPLICACION_INTERVALO - elapsed))
            except Exception as e:
                logger.error(f"Error en loop: {e}")
                time.sleep(REPLICACION_INTERVALO)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        logger.info("Servicio iniciado")

    def stop(self):
        logger.info("Deteniendo servicio...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)


service = None

def signal_handler(sig, frame):
    if service:
        service.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    service = ReplicacionService(modo=MODO, sucursal=SUCURSAL)
    service.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop()