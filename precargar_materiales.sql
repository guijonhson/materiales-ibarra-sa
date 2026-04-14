-- ============================================================
-- PRECARGA DE MATERIALES - SQLite
-- Materiales Ibarra, S.A.
-- Sucursales: Chiriquí, Veraguas, Chitré
-- ============================================================

-- ============================================================
-- 1. ELIMINAR TABLAS SI EXISTEN
-- ============================================================
DROP TABLE IF EXISTS cotizaciones;
DROP TABLE IF EXISTS materiales;

-- ============================================================
-- 2. CREAR TABLA: materiales
-- ============================================================
CREATE TABLE IF NOT EXISTS materiales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mongo_id TEXT UNIQUE,
    nombre TEXT NOT NULL UNIQUE,
    costo REAL NOT NULL CHECK(costo >= 0),
    cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
    descripcion TEXT,
    categoria TEXT,
    unidad TEXT,
    activo INTEGER DEFAULT 1,
    created_at TEXT,
    updated_at TEXT
);

-- ============================================================
-- 3. CREAR ÍNDICES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_materiales_nombre ON materiales(nombre);
CREATE INDEX IF NOT EXISTS idx_materiales_mongo_id ON materiales(mongo_id);
CREATE INDEX IF NOT EXISTS idx_materiales_categoria ON materiales(categoria);

-- ============================================================
-- 4. CREAR TABLA: cotizaciones
-- ============================================================
CREATE TABLE IF NOT EXISTS cotizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mongo_id TEXT,
    cliente_nombre TEXT NOT NULL,
    cliente_cedula TEXT,
    cliente_ruc TEXT,
    materiales TEXT NOT NULL,
    total REAL NOT NULL,
    sucursal TEXT DEFAULT 'CHIRIQUI',
    created_at TEXT,
    pdf_path TEXT,
    estado TEXT DEFAULT 'PENDIENTE'
);

-- ============================================================
-- 5. INSERTAR 60 MATERIALES
-- ============================================================

-- MATERIALES DE CONSTRUCCIÓN (1-10)
INSERT INTO materiales (nombre, costo, cantidad, descripcion, categoria, unidad, activo, created_at, updated_at) VALUES 
('Cemento Gris (42.5 kg)', 8.75, 500, 'Cemento Portland tipo I, saco de 42.5 kg', 'Construcción', 'saco', 1, datetime('now'), datetime('now')),
('Bloque de Concreto (hueco)', 0.90, 2000, 'Bloque estándar 20x20x40 cm', 'Construcción', 'pieza', 1, datetime('now'), datetime('now')),
('Arena Fina (m3)', 19.00, 150, 'Arena lavada para construcción', 'Construcción', 'm3', 1, datetime('now'), datetime('now')),
('Piedra Triturada (m3)', 23.50, 120, 'Piedra 3/4 para concreto', 'Construcción', 'm3', 1, datetime('now'), datetime('now')),
('Varilla Corrugada 3/8"', 13.75, 300, 'Acero de refuerzo Grado 60, 6m', 'Construcción', 'varilla', 1, datetime('now'), datetime('now')),
('Varilla Corrugada 1/2"', 18.50, 200, 'Acero de refuerzo Grado 60, 6m', 'Construcción', 'varilla', 1, datetime('now'), datetime('now')),
('Alambre de Amarre #18', 6.00, 150, 'Rollo de 5 kg', 'Construcción', 'rollo', 1, datetime('now'), datetime('now')),
('Clavo de 2" (kg)', 2.90, 80, 'Clavo acero galvanizado', 'Construcción', 'kg', 1, datetime('now'), datetime('now')),
('Clavo de 3" (kg)', 2.90, 75, 'Clavo acero galvanizado', 'Construcción', 'kg', 1, datetime('now'), datetime('now')),
('Madera Pino (pulgada)', 4.90, 400, 'Tabla 1" x 4" x 12 pies', 'Construcción', 'pieza', 1, datetime('now'), datetime('now'));

-- MATERIALES DE FERRETERÍA (11-20)
INSERT INTO materiales (nombre, costo, cantidad, descripcion, categoria, unidad, activo, created_at, updated_at) VALUES 
('Tubo PVC 1/2" (3m)', 3.75, 250, 'Tubería hidráulica blanca', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now')),
('Tubo PVC 3/4" (3m)', 4.50, 200, 'Tubería hidráulica blanca', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now')),
('Codo PVC 1/2"', 0.95, 500, 'Codo 90° para tubería', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now')),
('Tee PVC 1/2"', 1.20, 300, 'Conexión en T', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now')),
('Pegamento PVC (946ml)', 7.00, 60, 'Cemento para tuberías PVC', 'Ferretería', 'frasco', 1, datetime('now'), datetime('now')),
('Cinta Teflón (rollo)', 1.10, 200, 'Sellador para roscas', 'Ferretería', 'rollo', 1, datetime('now'), datetime('now')),
('Lija para Madera #100', 0.60, 150, 'Hoja de lija', 'Ferretería', 'hoja', 1, datetime('now'), datetime('now')),
('Brocha 2"', 2.25, 100, 'Brocha para pintura', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now')),
('Rodillo para Pintura 9"', 4.00, 80, 'Rodillo con mango', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now')),
('Bandeja para Pintura', 2.50, 70, 'Bandeja plástica', 'Ferretería', 'pieza', 1, datetime('now'), datetime('now'));

-- MATERIALES DE PINTURA (21-28)
INSERT INTO materiales (nombre, costo, cantidad, descripcion, categoria, unidad, activo, created_at, updated_at) VALUES 
('Pintura Latex Blanca (gal)', 26.00, 120, 'Pintura para interiores', 'Pintura', 'galón', 1, datetime('now'), datetime('now')),
('Pintura Esmalte Azul (gal)', 32.50, 60, 'Esmalte sintético', 'Pintura', 'galón', 1, datetime('now'), datetime('now')),
('Pintura Esmalte Rojo (gal)', 32.50, 55, 'Esmalte sintético', 'Pintura', 'galón', 1, datetime('now'), datetime('now')),
('Thinner (gal)', 14.00, 40, 'Diluyente', 'Pintura', 'galón', 1, datetime('now'), datetime('now')),
('Sellador (gal)', 17.00, 45, 'Primer para paredes', 'Pintura', 'galón', 1, datetime('now'), datetime('now')),
('Masilla (kg)', 5.00, 100, 'Para reparar paredes', 'Pintura', 'kg', 1, datetime('now'), datetime('now')),
('Espátula 4"', 3.00, 90, 'Para masilla', 'Pintura', 'pieza', 1, datetime('now'), datetime('now')),
('Cinta de Enmascarar (24mm)', 1.35, 200, 'Cinta的保护', 'Pintura', 'rollo', 1, datetime('now'), datetime('now'));

-- MATERIALES ELÉCTRICOS (29-38)
INSERT INTO materiales (nombre, costo, cantidad, descripcion, categoria, unidad, activo, created_at, updated_at) VALUES 
('Cable THHN #12 (100m)', 40.00, 50, 'Cable eléctrico calibre 12', 'Eléctrico', 'rollo', 1, datetime('now'), datetime('now')),
('Cable THHN #10 (100m)', 61.50, 35, 'Cable eléctrico calibre 10', 'Eléctrico', 'rollo', 1, datetime('now'), datetime('now')),
('Interruptor Sencillo', 2.80, 150, 'Interruptor 15A', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Toma Corriente Doble', 4.00, 140, 'Tomacorriente 15A', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Caja Octogonal 4x4"', 2.00, 200, 'Caja metálica', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Breaker 15A', 7.50, 80, 'Interruptor termomagnético', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Breaker 20A', 8.25, 70, 'Interruptor termomagnético', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Tubo Conduit EMT 1/2" (3m)', 5.20, 100, 'Tubería metálica', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Conector EMT 1/2"', 1.10, 300, 'Conector para tubería', 'Eléctrico', 'pieza', 1, datetime('now'), datetime('now')),
('Cinta Aislante Negra', 1.75, 180, 'Cinta vinílica', 'Eléctrico', 'rollo', 1, datetime('now'), datetime('now'));

-- HERRAMIENTAS (39-48)
INSERT INTO materiales (nombre, costo, cantidad, descripcion, categoria, unidad, activo, created_at, updated_at) VALUES 
('Martillo de Carpintero', 9.25, 50, 'Martillo de acero', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Destornillador Plano 6"', 4.25, 60, 'Destornillador plano', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Destornillador Phillips #2', 4.25, 60, 'Destornillador Phillips', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Llave Ajustable 8"', 13.00, 40, 'Llave perica', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Alicate de Presión', 10.50, 45, 'Alicate universal', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Cinta Métrica 5m', 5.50, 70, 'Cinta de acero', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Nivel de Burbuja 60cm', 8.50, 35, 'Nivel de aluminio', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Serrucho para Madera', 11.50, 30, 'Serrucho 20 pulgadas', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Flexómetro 8m', 7.00, 55, 'Flexómetro magnético', 'Herramientas', 'pieza', 1, datetime('now'), datetime('now')),
('Guantes de Carnaza (par)', 5.50, 80, 'Guantes de construcción', 'Herramientas', 'par', 1, datetime('now'), datetime('now'));

-- MATERIALES ESPECIALES (49-60)
INSERT INTO materiales (nombre, costo, cantidad, descripcion, categoria, unidad, activo, created_at, updated_at) VALUES 
('Mortero Preparado (40kg)', 8.25, 120, 'Mezcla lista', 'Especiales', 'saco', 1, datetime('now'), datetime('now')),
('Yeso (25kg)', 10.00, 90, 'Para acabados', 'Especiales', 'saco', 1, datetime('now'), datetime('now')),
('Geomembrana (m2)', 5.00, 500, 'Impermeabilización', 'Especiales', 'm2', 1, datetime('now'), datetime('now')),
('Malla Electrosoldada 5x5', 19.50, 60, 'Rollo 2x20m', 'Especiales', 'rollo', 1, datetime('now'), datetime('now')),
('Fibra de Vidrio (m2)', 4.20, 200, 'Refuerzos estructurales', 'Especiales', 'm2', 1, datetime('now'), datetime('now')),
('Adhesivo Cerámico (20kg)', 13.50, 80, 'Pegamento para baldosas', 'Especiales', 'saco', 1, datetime('now'), datetime('now')),
('Lechada para Cerámica (kg)', 2.75, 150, 'Juntas entre baldosas', 'Especiales', 'kg', 1, datetime('now'), datetime('now')),
('Polvo de Cemento Blanco (kg)', 2.00, 200, 'Acabados finos', 'Especiales', 'kg', 1, datetime('now'), datetime('now')),
('Cal Hidratada (25kg)', 8.75, 70, 'Para mortero', 'Especiales', 'saco', 1, datetime('now'), datetime('now')),
('Impermeabilizante (gal)', 20.00, 45, 'Líquido impermeabilizante', 'Especiales', 'galón', 1, datetime('now'), datetime('now')),
('Estuco Acrílico (gal)', 24.00, 55, 'Texturizado fachadas', 'Especiales', 'galón', 1, datetime('now'), datetime('now')),
('Sellador de Silicona (300ml)', 5.25, 120, 'Transparente', 'Especiales', 'tubo', 1, datetime('now'), datetime('now'));

-- ============================================================
-- 6. VERIFICACIÓN
-- ============================================================
SELECT '=== VERIFICACIÓN ===' AS '';
SELECT COUNT(*) AS total_materiales FROM materiales;

SELECT '=== MATERIALES POR CATEGORÍA ===' AS '';
SELECT categoria, COUNT(*) AS total FROM materiales GROUP BY categoria ORDER BY total DESC;

SELECT '=== RESUMEN DE PRECIOS ===' AS '';
SELECT 
    COUNT(*) AS total,
    MIN(costo) AS minimo,
    MAX(costo) AS maximo,
    AVG(costo) AS promedio
FROM materiales;