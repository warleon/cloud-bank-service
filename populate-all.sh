#!/bin/bash
# Script maestro para limpiar S3, poblar todas las BDs y ejecutar ingester

set -e  # Detener si hay error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 LIMPIEZA Y POBLACIÓN COMPLETA DEL SISTEMA BANCARIO    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install psycopg2-binary mysql-connector-python pymongo faker

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🧹 PASO 1: Limpiando buckets S3..."
echo "════════════════════════════════════════════════════════════"
bash cleanup-s3.sh

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📊 PASO 2: Poblando MS1 (PostgreSQL) - 20,000 clientes"
echo "════════════════════════════════════════════════════════════"
python3 populate_ms1.py

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📊 PASO 3: Poblando MS2 (MySQL) - 20,000 cuentas"
echo "════════════════════════════════════════════════════════════"
python3 populate_ms2.py

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📊 PASO 4: Poblando MS4 (MongoDB) - 20,000 transacciones"
echo "════════════════════════════════════════════════════════════"
python3 populate_ms4.py

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🔄 PASO 5: Ejecutando ingester para subir datos a S3..."
echo "════════════════════════════════════════════════════════════"
# Esto debe ejecutarse desde MS5
echo "⚠️  EJECUTA ESTO MANUALMENTE EN MS5:"
echo ""
echo "    ssh ubuntu@3.95.211.15"
echo "    cd ~/cloud-bank-service/ms5/datalake-ingester"
echo "    docker-compose run --rm datalake-ingester python run_ingestion.py"
echo ""

echo ""
echo "════════════════════════════════════════════════════════════"
echo "📋 PASO 6: Actualizar catálogo Athena"
echo "════════════════════════════════════════════════════════════"
echo "⚠️  EJECUTA ESTO MANUALMENTE:"
echo ""
echo "aws athena start-query-execution \\"
echo "  --query-string \"MSCK REPAIR TABLE cloud_bank_db.ms1_ms1_clientes;\" \\"
echo "  --result-configuration \"OutputLocation=s3://raw-ms1-data-bgc/athena-results/\" \\"
echo "  --query-execution-context \"Database=cloud_bank_db\" \\"
echo "  --region us-east-1"
echo ""
echo "aws athena start-query-execution \\"
echo "  --query-string \"MSCK REPAIR TABLE cloud_bank_db.ms2_ms2_cuentas;\" \\"
echo "  --result-configuration \"OutputLocation=s3://raw-ms2-data-bgc/athena-results/\" \\"
echo "  --query-execution-context \"Database=cloud_bank_db\" \\"
echo "  --region us-east-1"
echo ""
echo "aws athena start-query-execution \\"
echo "  --query-string \"MSCK REPAIR TABLE cloud_bank_db.ms4_ms4_transacciones;\" \\"
echo "  --result-configuration \"OutputLocation=s3://raw-ms4-data-bgc/athena-results/\" \\"
echo "  --query-execution-context \"Database=cloud_bank_db\" \\"
echo "  --region us-east-1"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ LIMPIEZA Y POBLACIÓN COMPLETADA                        ║"
echo "║                                                            ║"
echo "║  📊 Resumen:                                               ║"
echo "║     • 20,000 clientes en PostgreSQL (MS1)                 ║"
echo "║     • 20,000 cuentas en MySQL (MS2)                       ║"
echo "║     • 20,000 transacciones en MongoDB (MS4)               ║"
echo "║                                                            ║"
echo "║  🔄 Pendiente:                                             ║"
echo "║     1. Ejecutar ingester en MS5                           ║"
echo "║     2. Actualizar catálogo Athena (MSCK REPAIR)           ║"
echo "║     3. Reiniciar API Analytics                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
