cd ~/cloud-bank-service/ms5/datalake-ingester && docker-compose down -v && docker-compose down --remove-orphans && docker volume prune -f && docker image prune -f && docker-compose build --no-cache && docker-compose up -d && cd ../api-consultas && docker-compose down -v && docker-compose down --remove-orphans && docker-compose build --no-cache && docker-compose up -d && docker-compose logs -f#!/bin/bash

# Script para limpieza total y reinicio de todos los microservicios
# Ejecutar en cada EC2 según corresponda

set -e  # Detener en caso de error

echo "=============================================="
echo "🧹 LIMPIEZA TOTAL Y REINICIO DE MICROSERVICIOS"
echo "=============================================="
echo ""

# Función para limpiar y reiniciar un microservicio
cleanup_and_restart() {
    local MS_NAME=$1
    local MS_PATH=$2
    
    echo "----------------------------------------------"
    echo "📦 Procesando: $MS_NAME"
    echo "----------------------------------------------"
    
    if [ -d "$MS_PATH" ]; then
        cd "$MS_PATH"
        
        # 1. Detener contenedores
        echo "⏹️  Deteniendo contenedores..."
        docker-compose down -v 2>/dev/null || true
        
        # 2. Eliminar contenedores huérfanos
        echo "🗑️  Eliminando contenedores huérfanos..."
        docker-compose down --remove-orphans 2>/dev/null || true
        
        # 3. Limpiar volúmenes
        echo "💾 Limpiando volúmenes..."
        docker volume prune -f 2>/dev/null || true
        
        # 4. Limpiar imágenes dangling
        echo "🖼️  Limpiando imágenes no utilizadas..."
        docker image prune -f 2>/dev/null || true
        
        # 5. Reconstruir y levantar
        echo "🔨 Reconstruyendo imágenes..."
        docker-compose build --no-cache
        
        echo "🚀 Levantando servicios..."
        docker-compose up -d
        
        echo "✅ $MS_NAME completado!"
        echo ""
        
        # Esperar 5 segundos para que se inicialicen
        sleep 5
        
    else
        echo "⚠️  Directorio $MS_PATH no encontrado, saltando..."
        echo ""
    fi
}

# Actualizar repositorio
echo "📥 Actualizando código desde repositorio..."
cd ~/cloud-bank-service
git pull
echo ""

# Determinar qué microservicio limpiar según la ubicación
if [ -d "ms1" ]; then
    cleanup_and_restart "MS1 (Clientes - PostgreSQL)" "ms1"
fi

if [ -d "ms2" ]; then
    cleanup_and_restart "MS2 (Cuentas - MySQL)" "ms2"
fi

if [ -d "ms3" ]; then
    cleanup_and_restart "MS3 (API Gateway)" "ms3"
fi

if [ -d "ms4" ]; then
    cleanup_and_restart "MS4 (Transacciones - MongoDB)" "ms4"
fi

if [ -d "ms5/datalake-ingester" ]; then
    cleanup_and_restart "MS5 (DataLake Ingester)" "ms5/datalake-ingester"
fi

if [ -d "ms5/api-consultas" ]; then
    cleanup_and_restart "MS5 (API Consultas)" "ms5/api-consultas"
fi

# Mostrar estado final
echo "=============================================="
echo "📊 ESTADO FINAL DE CONTENEDORES"
echo "=============================================="
docker ps -a
echo ""

echo "=============================================="
echo "✅ LIMPIEZA Y REINICIO COMPLETADO"
echo "=============================================="
echo ""
echo "⏳ Esperando 10 segundos para que todo se inicialice..."
sleep 10

echo ""
echo "🔍 Verificando logs de los servicios..."
echo "Puedes ver los logs con: docker-compose logs -f"
