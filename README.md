# Materiales Ibarra, S.A. - Sistema de Gestión Integral

## Descripción
Prototipo CRUD completo para la gestión de materiales de construcción, cotizaciones y facturación fiscal (DGI) para Materiales Ibarra, S.A.

## Estructura del Proyecto

```
Materiales_Ibarra_S.A./
├── main.py                     # Punto de entrada original
├── iniciar.pyw                # ⚡ Iniciar con doble clic
├── iniciar.sh                  # Script para Linux
├── Materiales_Ibarra_S.A..desktop # Atajo para Linux
├── config/settings.py          # Configuración
├── db/                         # Bases de datos
│   ├── mongo.py               # MongoDB (Principal - No Relacional)
│   ├── sqlite_chiriqui.py     # SQLite Chiriquí (Relacional)
│   ├── sqlite_veraguas.py     # SQLite Veraguas (Relacional)
│   ├── sqlite_chitre.py       # SQLite Chitré (Relacional)
│   └── connection_manager.py  # Gestor de conexiones
├── models/                    # Modelos de datos
│   ├── material.py
│   ├── cotizacion.py
│   └── factura.py
├── repositories/              # Capa de acceso a datos (CRUD)
├── services/                  # Lógica de negocio
├── ui/                        # Interfaz gráfica (Tkinter)
│   ├── app_ui.py             # Menú principal
│   ├── admin_view.py         # Panel Administrador
│   ├── cliente_view.py       # Panel Cliente (Cotizaciones)
│   └── chatbot_view.py       # Chatbot interactivo
├── chatbot/                   # Chatbot con NLP
│   ├── bot.py
│   └── nlp_rules.py
├── utils/                    # Utilidades
│   ├── validators.py         # Validaciones (campos no nulos)
│   ├── formatters.py         # Formato 2 decimales
│   ├── logger.py             # Logging con Try-Catch
│   └── network_diagram.py    # Diagrama de red LAN
├── threads/                  # Replicación en tiempo real
├── tests/                    # Pruebas del sistema
│   ├── test_services.py
│   └── test_network.py
└── storage/                  # PDFs y backups
    ├── facturas/
    └── backups/
```

## Requisitos

```bash
pip install pymongo reportlab
```

## Cómo Ejecutar

### Opción 1: Doble Clic (Recomendado)
1. Dar permisos de ejecución al script:
   ```bash
   chmod +x iniciar.sh
   ```
2. Hacer doble clic en `iniciar.pyw` o `iniciar.sh`

### Opción 2: Terminal
```bash
python3 iniciar.pyw
# o
python3 main.py
```

## Características del Sistema

| Requisito | Estado | Descripción |
|-----------|--------|-------------|
| CRUD Funcional | ✓ | Create, Remove, Update, Delete |
| Interfaz Gráfica | ✓ | Tkinter con menús |
| Menú Admin/Cliente | ✓ | Panel separado por rol |
| Cotizaciones en Tiempo Real | ✓ | ComboBox + costo automático |
| Descarga PDF | ✓ | Generación y guardado en BD |
| Chatbot con Estadísticas | ✓ | NLP + stats del sistema |
| Facturación DGI | ✓ | XML emulate |
| 2 Cifras Decimales | ✓ | Todos los valores monetarios |
| Validación Try-Catch | ✓ | Manejo de errores |
| Campos No Nulos | ✓ | Validación de obligatorios |

## Base de Datos (3 Sucursales + Replicación)

| Base | Tipo | Ubicación |
|------|------|------------|
| MongoDB | No Relacional | localhost:27017 (Principal) |
| SQLite Chiriquí | Relacional | db/chiriqui.db |
| SQLite Veraguas | Relacional | db/veraguas.db |
| SQLite Chitré | Relacional | db/chitre.db |

**Replicación**: Cada 5 segundos los datos de MongoDB se copian a las 3 bases SQLite.

## Diagrama de Red LAN

```
        [Router]
           |
     [Switch VLAN 10]
      /     |      \
  CHIRQUI VERAGUAS CHITRE
  192.168.10.1  .2   .3
```

## Pruebas

```bash
python3 tests/test_services.py
python3 tests/test_network.py
```

## Sucursales
- Chiriquí (Principal) - Vía Panamericana
- Veraguas - Frente al Mall de Santiago
- Chitré - Frente al Hotel Gran Azuero