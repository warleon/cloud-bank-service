#!/bin/bash

# Script maestro para desplegar todos los microservicios
# Autor: Cloud Bank Service
# Fecha: 2025-10-05

set -e  # Detener si hay errores

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================"
echo "🚀 DESPLIEGUE AUTOMÁTICO - CLOUD BANK SERVICES"
echo "================================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para verificar que Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        exit 1
    fi
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose no está instalado${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker y Docker Compose disponibles${NC}"
}

# Función para desplegar un microservicio
deploy_microservice() {
    local MS_NAME=$1
    local MS_DIR=$2
    
    echo ""
    echo -e "${YELLOW}================================================${NC}"
    echo -e "${YELLOW}📦 Desplegando $MS_NAME${NC}"
    echo -e "${YELLOW}================================================${NC}"
    
    cd "$SCRIPT_DIR/$MS_DIR"
    
    # Bajar contenedores anteriores si existen
    echo "🔄 Deteniendo contenedores previos (si existen)..."
    docker-compose down 2>/dev/null || true
    
    # Levantar servicios
    echo "🚀 Iniciando servicios..."
    docker-compose up -d --build
    
    # Esperar unos segundos
    echo "⏳ Esperando inicialización..."
    sleep 10
    
    # Mostrar estado
    echo "📊 Estado de contenedores:"
    docker-compose ps
    
    echo -e "${GREEN}✅ $MS_NAME desplegado${NC}"
}

# Verificar requisitos
check_docker

# Desplegar MS1 - Clientes (Python + PostgreSQL)
deploy_microservice "MS1 - Gestión de Clientes" "ms1"

# Desplegar MS2 - Cuentas (Node.js + MySQL)
deploy_microservice "MS2 - Gestión de Cuentas" "ms2"

# Desplegar MS4 - Transacciones (Java + MongoDB)
echo ""
echo -e "${YELLOW}================================================${NC}"
echo -e "${YELLOW}📦 Desplegando MS4 - Transacciones${NC}"
echo -e "${YELLOW}⚠️  IMPORTANTE: Este proceso tarda 5-10 minutos${NC}"
echo -e "${YELLOW}================================================${NC}"
deploy_microservice "MS4 - Gestión de Transacciones" "ms4"

# Resumen final
echo ""
echo "================================================"
echo -e "${GREEN}✅ DESPLIEGUE COMPLETADO${NC}"
echo "================================================"
echo ""
echo "📋 Servicios desplegados:"
echo ""
echo "  🐍 MS1 - Clientes:      http://localhost:8001"
echo "  📊 Swagger MS1:         http://localhost:8001/docs"
echo ""
echo "  🟢 MS2 - Cuentas:       http://localhost:8002"
echo ""
echo "  ☕ MS4 - Transacciones: http://localhost:8004"
echo ""
echo "================================================"
echo ""
echo "🔍 Para verificar el estado de todos los servicios:"
echo ""
echo "  cd $SCRIPT_DIR/ms1 && docker-compose ps"
echo "  cd $SCRIPT_DIR/ms2 && docker-compose ps"
echo "  cd $SCRIPT_DIR/ms4 && docker-compose ps"
echo ""
echo "📝 Para ver logs:"
echo ""
echo "  docker-compose -f $SCRIPT_DIR/ms1/docker-compose.yml logs -f"
echo "  docker-compose -f $SCRIPT_DIR/ms2/docker-compose.yml logs -f"
echo "  docker-compose -f $SCRIPT_DIR/ms4/docker-compose.yml logs -f"
echo ""
echo "================================================"
