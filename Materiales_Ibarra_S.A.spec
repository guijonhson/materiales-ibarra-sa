# -*- mode: python ; coding: utf-8 -*-

import os
import shutil
from PyInstaller.utils.hooks import collect_all, collect_data_files

# Crear carpetas necesarias para el ejecutable
base_dir = os.path.dirname(os.path.abspath(SPEC))
db_source = os.path.join(base_dir, 'db')
storage_source = os.path.join(base_dir, 'storage')

# Verificar que existan las carpetas fuente
if not os.path.exists(db_source):
    os.makedirs(db_source, exist_ok=True)
if not os.path.exists(storage_source):
    os.makedirs(storage_source, exist_ok=True)

# Incluir carpetas	db	y storage	directamente (force add)
datas = []
datas.append((db_source, 'db'))
datas.append((storage_source, 'storage'))

a = Analysis(
    ['iniciar.pyw'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'services.facturacion_service',
        'services.cotizacion_service',
        'services.material_service',
        'services.pdf_service',
        'services.stats_service',
        'services.replicacion_service',
        'repositories.material_repo',
        'repositories.cotizacion_repo',
        'repositories.pdf_repo',
        'db.mongo',
        'db.sqlite_chiriqui',
        'db.sqlite_veraguas',
        'db.connection_manager',
        'chatbot.bot',
        'chatbot.nlp_rules',
        'models.material',
        'models.cotizacion',
        'models.factura',
        'utils.validators',
        'utils.formatters',
        'utils.logger',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Materiales_Ibarra_S.A',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
