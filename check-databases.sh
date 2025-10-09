#!/bin/bash

# Script para verificar el estado de las bases de datos
# Ejecutar desde cada instancia EC2 respectiva

echo "=========================================="
echo "VERIFICACIÓN DE BASES DE DATOS"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# MS1 - PostgreSQL (Clientes)
echo -e "${YELLOW}[MS1] PostgreSQL - Clientes${NC}"
echo "--------------------------------------------"
PGPASSWORD=admin123 psql -h localhost -U admin -d clientes_db -c "
SELECT 
    'clientes' as tabla,
    COUNT(*) as total_registros
FROM clientes
UNION ALL
SELECT 
    'documentos_identidad' as tabla,
    COUNT(*) as total_registros
FROM documentos_identidad;
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ MS1 PostgreSQL: CONECTADO${NC}"
else
    echo -e "${RED}✗ MS1 PostgreSQL: ERROR DE CONEXIÓN${NC}"
fi
echo ""

# MS2 - MySQL (Cuentas)
echo -e "${YELLOW}[MS2] MySQL - Cuentas${NC}"
echo "--------------------------------------------"
mysql -h localhost -u admin -padmin123 -D cuentas_db -e "
SELECT 'cuentas' as tabla, COUNT(*) as total_registros FROM cuentas
UNION ALL
SELECT 'tipos_cuenta' as tabla, COUNT(*) as total_registros FROM tipos_cuenta;
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ MS2 MySQL: CONECTADO${NC}"
else
    echo -e "${RED}✗ MS2 MySQL: ERROR DE CONEXIÓN${NC}"
fi
echo ""

# MS4 - MongoDB (Transacciones)
echo -e "${YELLOW}[MS4] MongoDB - Transacciones${NC}"
echo "--------------------------------------------"
mongosh mongodb://admin:admin123@localhost:27017/transacciones_db --authenticationDatabase admin --quiet --eval "
print('Collection: transacciones');
print('Total registros: ' + db.transacciones.countDocuments());
print('');
print('Muestra de estados:');
db.transacciones.aggregate([
    { \$group: { _id: '\$estado', count: { \$sum: 1 } } },
    { \$sort: { count: -1 } }
]).forEach(doc => print('  ' + doc._id + ': ' + doc.count));
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ MS4 MongoDB: CONECTADO${NC}"
else
    echo -e "${RED}✗ MS4 MongoDB: ERROR DE CONEXIÓN${NC}"
fi
echo ""

echo "=========================================="
echo "VERIFICACIÓN COMPLETA"
echo "=========================================="
