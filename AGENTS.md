# AGENTS.md - Materiales Ibarra, S.A.

> Agentic coding guidelines for this codebase.

---

## 1. Quick Start

### Development
```bash
# Activate venv (Windows)
venv\Scripts\activate.bat

# Run directly
python iniciar.pyw
```

### Testing
```bash
# Run all tests
python tests/test_services.py

# Run single test with pytest
python -m pytest tests/test_services.py::test_mongodb_connection -v
```

### Build
```bash
# Create venv
python -m venv venv

# Install dependencies
venv\Scripts\pip.exe install pymongo reportlab pyinstaller

# Build executable
pyinstaller Materiales_Ibarra_S.A.spec --clean
```

---

## 2. Architecture

### Database Layout
| Type | Location | Purpose |
|------|----------|---------|
| **MongoDB** | localhost:27017 | Primary DB (`materiales_ibarra`) |
| **SQLite Chiriqui** | `db/chiriqui.db` | Replica for Chiriqui branch |
| **SQLite Veraguas** | `db/veraguas.db` | Replica for Veraguas branch |
| **SQLite Chitré** | `db/chitre.db` | Replica for Chitré branch |

### UI Entry Points
| File | Description |
|------|-------------|
| `ui/app_ui.py` | Main menu (Admin/Cliente/Chatbot) |
| `ui/admin_view.py` | Admin panel (CRUD materials) |
| `ui/cliente_view.py` | Client panel (cotizaciones) |
| `ui/chatbot_view.py` | Interactive chatbot |

---

## 3. Critical Gotchas

### MongoDB Field Name Mismatch
Always use both field names:
```python
precio = doc.get("costo") or doc.get("precio") or 0
```

### BASE_DIR Resolution
Always import from `config.settings`:
```python
from config.settings import BASE_DIR  # Correct
# NOT from Config.BASE_DIR
```

### Storage Paths
- PDFs: `BASE_DIR/storage/facturas/cotizacion_YYYYMMDD/`
- SQLite: `BASE_DIR/db/chiriqui.db`, etc.

---

## 4. Code Style Guidelines

### Imports (order matters)
```python
# 1. Standard library
import os
import sys
from typing import List, Optional
from datetime import datetime

# 2. Third-party
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# 3. Local project
from config.settings import Config, BASE_DIR
from models.material import Material
```

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Modules | `snake_case` | `material_repo.py` |
| Classes | `PascalCase` | `MaterialService` |
| Functions | `snake_case` | `get_all_materials()` |
| Constants | `UPPER_SNAKE` | `MAX_CONNECTIONS` |

### Type Hints (required for public APIs)
```python
def get_material(material_id: str) -> Optional[Material]:
    pass

def find_by_name(name: str) -> List[Material]:
    return []
```

### Error Handling
```python
try:
    result = collection.insert_one(doc)
except ConnectionFailure as e:
    logger.error(f"MongoDB connection failed: {e}")
    return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Logging
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug info")
logger.info("Normal operation")
logger.warning("Unexpected but recoverable")
logger.error("Serious problem")
```

---

## 5. Project Structure

```
Materiales_Ibarra_S.A/
├── config/settings.py          # Central config (BASE_DIR detection)
├── db/
│   ├── mongo.py                # MongoDB connection
│   ├── sqlite_chiriqui.py      # SQLite replica
│   ├── sqlite_veraguas.py       # SQLite replica
│   └── sqlite_chitre.py         # SQLite replica
├── models/
│   ├── material.py             # Material model
│   ├── cotizacion.py           # Cotizacion model
│   └── factura.py              # Factura model
├── repositories/               # Data access layer
├── services/                   # Business logic layer
├── ui/                         # Tkinter UI
├── chatbot/                    # Chatbot NLP
├── storage/facturas/           # Generated PDFs
├── tests/                      # Test suite
└── iniciar.pyw                 # Entry point
```

---

## 6. Testing

```bash
# Run all tests
python tests/test_services.py

# Run single test
python -m pytest tests/test_services.py::test_mongodb_connection -v
```

---

## 7. MongoDB Operations

### Start/Stop MongoDB (Windows)
```cmd
sc start MongoDB
sc query MongoDB
sc stop MongoDB
```

### Verify Connection
```bash
python -c "from pymongo import MongoClient; print(client.admin.command('ping'))"
```

---

## 8. Cleanup Scripts

```bash
# Clean all databases and generated files
python scripts\limpieza_rapida.py --force
```