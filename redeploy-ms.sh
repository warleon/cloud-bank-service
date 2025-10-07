#!/bin/bash

# Script de re-despliegue rápido después de cambios en el código
# Uso: ./redeploy-ms.sh [ms1|ms2|ms3|ms4|ms5]

MS=$1

if [ -z "$MS" ]; then
    echo "❌ Error: Especifica el microservicio a redesplegar"
    echo "Uso: ./redeploy-ms.sh [ms1|ms2|ms3|ms4|ms5]"
    exit 1
fi

echo "🔄 Redesplegando $MS..."

cd ~/ cloud-bank-service/$MS

# Pull últimos cambios
git pull origin main

# Reconstruir y reiniciar contenedores
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "✅ $MS redesplegado exitosamente"
echo "📊 Verificando logs..."
docker-compose logs --tail=50
