# -*- coding: utf-8 -*-
# -*- mode: python -*-

import sys
import os

block_cipher = None

# Añadir el directorio actual
CURRENT_DIR = os.path.dirname(os.path.abspath(SPEC))

# Archivos de datos a incluir
datas = [
    (os.path.join(CURRENT_DIR, 'config'), 'config'),
    (os.path.join(CURRENT_DIR, 'models'), 'models'),
    (os.path.join(CURRENT_DIR, 'chatbot'), 'chatbot'),
    (os.path.join(CURRENT_DIR, 'utils'), 'utils'),
    (os.path.join(CURRENT_DIR, 'storage'), 'storage'),
]

a = Analysis(
    [os.path.join(CURRENT_DIR, 'iniciar.pyw')],
    pathex=[CURRENT_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pymongo',
        'reportlab',
        'tkinter',
        'bson',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Materiales_Ibarra_S.A',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola (interfaz gráfica)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)