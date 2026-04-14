// ============================================================
// PRECARGA DE MATERIALES - MongoDB
// Materiales Ibarra, S.A.
// ============================================================

use('materiales_ibarra');

// ============================================================
// 1. LIMPIAR COLECCIÓN EXISTENTE
// ============================================================
print("\n=== LIMPIANDO COLECCIONES ===");
db.materiales.deleteMany({});
db.cotizaciones.deleteMany({});
db.facturas.deleteMany({});
print("✓ Colecciones limpiadas");

// ============================================================
// 2. VERIFICAR Y CREAR ÍNDICES (solo si no existen)
// ============================================================
print("\n=== CREANDO ÍNDICES ===");

// Índice en nombre (único)
try { db.materiales.createIndex({nombre: 1}, {unique: true, name: "idx_nombre"}); print("✓ Índice en nombre creado"); } catch(e) { /* ya existe */ }

// Índice en categoría
try { db.materiales.createIndex({categoria: 1}, {name: "idx_categoria"}); print("✓ Índice en categoria creado"); } catch(e) { /* ya existe */ }

// Índice en costo
try { db.materiales.createIndex({costo: 1}, {name: "idx_costo"}); print("✓ Índice en costo creado"); } catch(e) { /* ya existe */ }

// ============================================================
// 3. INSERTAR 60 MATERIALES
// ============================================================
print("\n=== INSERTANDO MATERIALES ===");

var materiales = [
// MATERIALES DE CONSTRUCCIÓN (1-10)
{
    nombre: "Cemento Gris (42.5 kg)",
    costo: 8.75,
    cantidad: 500,
    descripcion: "Cemento Portland tipo I, saco de 42.5 kg. Precio referencial Chiriquí 2026",
    categoria: "Construcción",
    unidad: "saco",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Bloque de Concreto (hueco)",
    costo: 0.90,
    cantidad: 2000,
    descripcion: "Bloque estándar 20x20x40 cm. Para muros de carga y divisiones",
    categoria: "Construcción",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Arena Fina (m³)",
    costo: 19.00,
    cantidad: 150,
    descripcion: "Arena lavada para construcción. Precio por metro cúbico",
    categoria: "Construcción",
    unidad: "m3",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Piedra Triturada (m³)",
    costo: 23.50,
    cantidad: 120,
    descripcion: "Piedra 3/4 para concreto estructural",
    categoria: "Construcción",
    unidad: "m3",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Varilla Corrugada 3/8\"",
    costo: 13.75,
    cantidad: 300,
    descripcion: "Acero de refuerzo Grado 60, longitud 6 metros",
    categoria: "Construcción",
    unidad: "varilla",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Varilla Corrugada 1/2\"",
    costo: 18.50,
    cantidad: 200,
    descripcion: "Acero de refuerzo Grado 60, longitud 6 metros",
    categoria: "Construcción",
    unidad: "varilla",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Alambre de Amarre #18",
    costo: 6.00,
    cantidad: 150,
    descripcion: "Rollo de 5 kg. Para amarre de varillas",
    categoria: "Construcción",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Clavo de 2\" (kg)",
    costo: 2.90,
    cantidad: 80,
    descripcion: "Clavo acero galvanizado. Precio por kilogramo",
    categoria: "Construcción",
    unidad: "kg",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Clavo de 3\" (kg)",
    costo: 2.90,
    cantidad: 75,
    descripcion: "Clavo acero galvanizado. Precio por kilogramo",
    categoria: "Construcción",
    unidad: "kg",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Madera Pino (pulgada)",
    costo: 4.90,
    cantidad: 400,
    descripcion: "Tabla de 1\" x 4\" x 12 pies. Para encofrados y estructuras temporales",
    categoria: "Construcción",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},

// MATERIALES DE FERRETERÍA (11-20)
{
    nombre: "Tubo PVC 1/2\" (3m)",
    costo: 3.75,
    cantidad: 250,
    descripcion: "Tubería hidráulica blanca, 3 metros. Para instalaciones de agua potable",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Tubo PVC 3/4\" (3m)",
    costo: 4.50,
    cantidad: 200,
    descripcion: "Tubería hidráulica blanca, 3 metros",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Codo PVC 1/2\"",
    costo: 0.95,
    cantidad: 500,
    descripcion: "Codo 90° para tubería de agua",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Tee PVC 1/2\"",
    costo: 1.20,
    cantidad: 300,
    descripcion: "Conexión en T para derivaciones",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Pegamento PVC (946ml)",
    costo: 7.00,
    cantidad: 60,
    descripcion: "Cemento para tuberías PVC. Frasco de 946 ml",
    categoria: "Ferretería",
    unidad: "frasco",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Cinta Teflón (rollo)",
    costo: 1.10,
    cantidad: 200,
    descripcion: "Sellador para roscas. Rollo estándar",
    categoria: "Ferretería",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Lija para Madera #100",
    costo: 0.60,
    cantidad: 150,
    descripcion: "Hoja de lija para acabados",
    categoria: "Ferretería",
    unidad: "hoja",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Brocha 2\"",
    costo: 2.25,
    cantidad: 100,
    descripcion: "Brocha para pintura. Cerdas mixtas",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Rodillo para Pintura 9\"",
    costo: 4.00,
    cantidad: 80,
    descripcion: "Rodillo con mango y esponja para pintura",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Bandeja para Pintura",
    costo: 2.50,
    cantidad: 70,
    descripcion: "Bandeja plástica para rodillo de 9\"",
    categoria: "Ferretería",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},

// MATERIALES DE PINTURA Y ACABADOS (21-28)
{
    nombre: "Pintura Latex Blanca (gal)",
    costo: 26.00,
    cantidad: 120,
    descripcion: "Pintura para interiores, lavable y durable",
    categoria: "Pintura",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Pintura Esmalte Azul (gal)",
    costo: 32.50,
    cantidad: 60,
    descripcion: "Esmalte sintético para exteriores y metales",
    categoria: "Pintura",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Pintura Esmalte Rojo (gal)",
    costo: 32.50,
    cantidad: 55,
    descripcion: "Esmalte sintético para exteriores y metales",
    categoria: "Pintura",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Thinner (gal)",
    costo: 14.00,
    cantidad: 40,
    descripcion: "Diluyente para esmaltes y limpieza",
    categoria: "Pintura",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Sellador (gal)",
    costo: 17.00,
    cantidad: 45,
    descripcion: "Primer para paredes antes de pintar",
    categoria: "Pintura",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Masilla (kg)",
    costo: 5.00,
    cantidad: 100,
    descripcion: "Para reparar imperfecciones en paredes",
    categoria: "Pintura",
    unidad: "kg",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Espátula 4\"",
    costo: 3.00,
    cantidad: 90,
    descripcion: "Para aplicar masilla y acabados",
    categoria: "Pintura",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Cinta de Enmascarar (24mm)",
    costo: 1.35,
    cantidad: 200,
    descripcion: "Cinta para protección en pintura",
    categoria: "Pintura",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},

// MATERIALES ELÉCTRICOS (29-38)
{
    nombre: "Cable THHN #12 (100m)",
    costo: 40.00,
    cantidad: 50,
    descripcion: "Cable eléctrico calibre 12, rollo 100m. Para tomacorrientes",
    categoria: "Eléctrico",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Cable THHN #10 (100m)",
    costo: 61.50,
    cantidad: 35,
    descripcion: "Cable eléctrico calibre 10, rollo 100m. Para circuitos de alta demanda",
    categoria: "Eléctrico",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Interruptor Sencillo",
    costo: 2.80,
    cantidad: 150,
    descripcion: "Interruptor 15A, blanco",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Toma Corriente Doble",
    costo: 4.00,
    cantidad: 140,
    descripcion: "Tomacorriente 15A con puesta a tierra",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Caja Octogonal 4x4\"",
    costo: 2.00,
    cantidad: 200,
    descripcion: "Caja metálica para conexiones eléctricas",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Breaker 15A",
    costo: 7.50,
    cantidad: 80,
    descripcion: "Interruptor termomagnético 15A para tablero",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Breaker 20A",
    costo: 8.25,
    cantidad: 70,
    descripcion: "Interruptor termomagnético 20A para tablero",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Tubo Conduit EMT 1/2\" (3m)",
    costo: 5.20,
    cantidad: 100,
    descripcion: "Tubería metálica para instalaciones eléctricas",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Conector EMT 1/2\"",
    costo: 1.10,
    cantidad: 300,
    descripcion: "Conector para tubería EMT",
    categoria: "Eléctrico",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Cinta Aislante Negra",
    costo: 1.75,
    cantidad: 180,
    descripcion: "Cinta vinílica 3M para aislamiento eléctrico",
    categoria: "Eléctrico",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},

// HERRAMIENTAS (39-48)
{
    nombre: "Martillo de Carpintero",
    costo: 9.25,
    cantidad: 50,
    descripcion: "Martillo de acero con mango de madera",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Destornillador Plano 6\"",
    costo: 4.25,
    cantidad: 60,
    descripcion: "Destornillador plano punta magnética",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Destornillador Phillips #2",
    costo: 4.25,
    cantidad: 60,
    descripcion: "Destornillador Phillips punta magnética",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Llave Ajustable 8\"",
    costo: 13.00,
    cantidad: 40,
    descripcion: "Llave perica de 8 pulgadas",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Alicate de Presión",
    costo: 10.50,
    cantidad: 45,
    descripcion: "Alicate universal para agarre y corte",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Cinta Métrica 5m",
    costo: 5.50,
    cantidad: 70,
    descripcion: "Cinta de acero de 5 metros",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Nivel de Burbuja 60cm",
    costo: 8.50,
    cantidad: 35,
    descripcion: "Nivel de aluminio con 3 burbujas",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Serrucho para Madera",
    costo: 11.50,
    cantidad: 30,
    descripcion: "Serrucho con hoja de 20 pulgadas",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Flexómetro 8m",
    costo: 7.00,
    cantidad: 55,
    descripcion: "Flexómetro con freno y gancho magnético",
    categoria: "Herramientas",
    unidad: "pieza",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Guantes de Carnaza (par)",
    costo: 5.50,
    cantidad: 80,
    descripcion: "Guantes de carnaza para construcción",
    categoria: "Herramientas",
    unidad: "par",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},

// MATERIALES ESPECIALES (49-60)
{
    nombre: "Mortero Preparado (40kg)",
    costo: 8.25,
    cantidad: 120,
    descripcion: "Mezcla lista para pegar bloques y repellar",
    categoria: "Especiales",
    unidad: "saco",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Yeso (25kg)",
    costo: 10.00,
    cantidad: 90,
    descripcion: "Para acabados de paredes y cielorrasos",
    categoria: "Especiales",
    unidad: "saco",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Geomembrana (m²)",
    costo: 5.00,
    cantidad: 500,
    descripcion: "Para impermeabilización de techos y terrazas",
    categoria: "Especiales",
    unidad: "m2",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Malla Electrosoldada 5x5",
    costo: 19.50,
    cantidad: 60,
    descripcion: "Rollo de 2x20 metros. Para refuerzo de concretos",
    categoria: "Especiales",
    unidad: "rollo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Fibra de Vidrio (m²)",
    costo: 4.20,
    cantidad: 200,
    descripcion: "Para refuerzos estructurales e impermeabilización",
    categoria: "Especiales",
    unidad: "m2",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Adhesivo Cerámico (20kg)",
    costo: 13.50,
    cantidad: 80,
    descripcion: "Pegamento para baldosas y cerámicas",
    categoria: "Especiales",
    unidad: "saco",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Lechada para Cerámica (kg)",
    costo: 2.75,
    cantidad: 150,
    descripcion: "Para juntas entre baldosas",
    categoria: "Especiales",
    unidad: "kg",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Polvo de Cemento Blanco (kg)",
    costo: 2.00,
    cantidad: 200,
    descripcion: "Para acabados finos y detalles decorativos",
    categoria: "Especiales",
    unidad: "kg",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Cal Hidratada (25kg)",
    costo: 8.75,
    cantidad: 70,
    descripcion: "Para mezclas de mortero y acabados",
    categoria: "Especiales",
    unidad: "saco",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Impermeabilizante (gal)",
    costo: 20.00,
    cantidad: 45,
    descripcion: "Líquido para impermeabilizar muros y techos",
    categoria: "Especiales",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Estuco Acrílico (gal)",
    costo: 24.00,
    cantidad: 55,
    descripcion: "Acabado texturizado para fachadas",
    categoria: "Especiales",
    unidad: "galón",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
},
{
    nombre: "Sellador de Silicona (300ml)",
    costo: 5.25,
    cantidad: 120,
    descripcion: "Transparente, para baños y cocinas",
    categoria: "Especiales",
    unidad: "tubo",
    activo: true,
    created_at: new Date(),
    updated_at: new Date()
}
];

// Insertar materiales
var result = db.materiales.insertMany(materiales);
print("\n✓ " + result.insertedCount + " materiales insertados en MongoDB");

// ============================================================
// 4. VERIFICACIÓN
// ============================================================
print("\n=== VERIFICACIÓN ===");
print("Total materiales: " + db.materiales.countDocuments({}));

// Precios
print("\n=== MATERIALES CON PRECIOS (primeros 10) ===");
db.materiales.find({}, {nombre: 1, costo: 1, cantidad: 1, descripcion: 1}).limit(10).forEach(function(doc) {
    print(doc.nombre + " - $" + doc.costo + " - Stock: " + doc.cantidad);
});

// Resumen
print("\n=== RESUMEN DE PRECIOS ===");
var stats = db.materiales.aggregate([
    {$group: {
        _id: null,
        total: {$sum: 1},
        minimo: {$min: "$costo"},
        maximo: {$max: "$costo"},
        promedio: {$avg: "$costo"}
    }}
]);
stats.forEach(function(doc) {
    print("Total materiales: " + doc.total);
    print("Precio mínimo: $" + doc.minimo);
    print("Precio máximo: $" + doc.maximo);
    print("Precio promedio: $" + doc.promedio.toFixed(2));
});

// Por categoría
print("\n=== MATERIALES POR CATEGORÍA ===");
var porCategoria = db.materiales.aggregate([
    {$group: {_id: "$categoria", total: {$sum: 1}}},
    {$sort: {total: -1}}
]);
porCategoria.forEach(function(doc) {
    print(doc._id + ": " + doc.total);
});

print("\n=== PRECARGA COMPLETADA ===");