# -*- coding: utf-8 -*-
"""
Hilo de Sincronización - Replicación en Tiempo Real
Materiales Ibarra, S.A.
"""

import threading
import time
from services.replicacion_service import replicacion_service
import logging

logger = logging.getLogger(__name__)

class SyncThread:
    """Hilo para sincronización en tiempo real"""
    
    def __init__(self):
        self.thread = None
        self.running = False
    
    def start(self):
        """Inicia el hilo de sincronización"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            logger.info("✓ Hilo de sincronización iniciado")
    
    def stop(self):
        """Detiene el hilo de sincronización"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("✗ Hilo de sincronización detenido")
    
    def _run(self):
        """Ejecuta la sincronización"""
        while self.running:
            try:
                replicacion_service.forzar_sincronizacion()
                time.sleep(10)
            except Exception as e:
                logger.error(f"Error en sync thread: {e}")

sync_thread = SyncThread()