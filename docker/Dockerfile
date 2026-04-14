# docker/Dockerfile
# Imagen para el servicio de réplicas de Materiales Ibarra, S.A.
# Respetando AGENTS.md: MongoDB permanece en Windows

FROM python:3.11-slim

LABEL maintainer="Materiales Ibarra, S.A."
LABEL description="Servicio de réplicas SQLite (MongoDB en Windows)"
LABEL version="1.0"

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Panama

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY replicador/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY replicador/replicacion_service.py .
COPY replicador/health_check.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh health_check.py
RUN mkdir -p /data/chiriqui /data/veraguas /data/chitre

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 health_check.py || exit 1

ENTRYPOINT ["./entrypoint.sh"]