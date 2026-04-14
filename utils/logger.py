# -*- coding: utf-8 -*-
"""
Logger - Sistema de Logging
Materiales Ibarra, S.A.
"""

import logging
import os
from datetime import datetime
from config.settings import Config, BASE_DIR

def setup_logger(name: str = "MaterialesIbarra") -> logging.Logger:
    """Configura el logger de la aplicación"""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    log_file = os.path.join(BASE_DIR, "app.log")
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass
    
    return logger

logger = setup_logger()

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)

def log_warning(message: str):
    logger.warning(message)

def log_debug(message: str):
    logger.debug(message)