@echo off
chcp 65001 >nul
title Limpiar MongoDB - Materiales Ibarra, S.A.
echo ============================================
echo LIMPIEZA DE MONGODB
echo ============================================
echo.
echo Conectando a MongoDB localhost:27017...
echo.

mongosh --quiet --eval "
use materiales_ibarra;
print('=== Antes de limpiar ===');
print('  Materiales: ' + db.materiales.countDocuments({}));
print('  Cotizaciones: ' + db.cotizaciones.countDocuments({}));
print('  Facturas: ' + db.facturas.countDocuments({}));
print('');
db.materiales.deleteMany({});
db.cotizaciones.deleteMany({});
db.facturas.deleteMany({});
print('=== Despues de limpiar ===');
print('  Materiales: ' + db.materiales.countDocuments({}));
print('  Cotizaciones: ' + db.cotizaciones.countDocuments({}));
print('  Facturas: ' + db.facturas.countDocuments({}));
"

echo.
echo ============================================
echo LIMPIEZA COMPLETADA
echo ============================================
pause