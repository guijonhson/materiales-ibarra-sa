@echo off
chcp 65001 >nul
title Precargar Materiales - MongoDB
echo ============================================
echo PRECARGA DE MATERIALES
echo Materiales Ibarra, S.A.
echo ============================================
echo.
echo Conectando a MongoDB localhost:27017...
echo.

REM Ejecutar script de precarga
mongosh --quiet materiales_ibarra precargar_materiales.js

echo.
echo ============================================
echo PRECARGA COMPLETADA
echo ============================================
pause