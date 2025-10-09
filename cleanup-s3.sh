#!/bin/bash
# Script para limpiar todos los datos antiguos de los buckets S3

echo "🧹 Limpiando buckets S3..."

# Bucket MS1 (Clientes - PostgreSQL)
echo "Limpiando raw-ms1-data-bgc..."
aws s3 rm s3://raw-ms1-data-bgc/ms1_clientes/ --recursive
aws s3 rm s3://raw-ms1-data-bgc/ms1_documentos_identidad/ --recursive

# Bucket MS2 (Cuentas - MySQL)
echo "Limpiando raw-ms2-data-bgc..."
aws s3 rm s3://raw-ms2-data-bgc/ms2_cuentas/ --recursive
aws s3 rm s3://raw-ms2-data-bgc/ms2_tipos_cuenta/ --recursive

# Bucket MS4 (Transacciones - MongoDB)
echo "Limpiando raw-ms4-data-bgc..."
aws s3 rm s3://raw-ms4-data-bgc/ms4_transacciones/ --recursive
aws s3 rm s3://raw-ms4-data-bgc/ms4_metadata/ --recursive

echo "✅ Limpieza completada"
echo ""
echo "📊 Verificando estado de los buckets:"
aws s3 ls s3://raw-ms1-data-bgc/ --recursive | wc -l
aws s3 ls s3://raw-ms2-data-bgc/ --recursive | wc -l
aws s3 ls s3://raw-ms4-data-bgc/ --recursive | wc -l
