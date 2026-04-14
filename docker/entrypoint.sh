#!/bin/bash
set -e

echo "=========================================="
echo "Materiales Ibarra, S.A. - Servicio de Replicas"
echo "=========================================="
echo "Modo: $MODO"
echo "MongoDB: ${MONGO_HOST:-host.docker.internal}:${MONGO_PORT:-27017}"
echo "=========================================="

exec python3 replicacion_service.py