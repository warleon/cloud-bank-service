# Script para verificar la estructura de S3
# Ejecutar desde EC2 MS5 o tu máquina local con AWS CLI configurado

echo "=== Verificando estructura en raw-ms4-data-bgc ==="
aws s3 ls s3://raw-ms4-data-bgc/ --recursive

echo ""
echo "=== Carpetas de primer nivel ==="
aws s3 ls s3://raw-ms4-data-bgc/

echo ""
echo "=== Comparando con MS1 ==="
aws s3 ls s3://raw-ms1-data-bgc/

echo ""
echo "=== Comparando con MS2 ==="
aws s3 ls s3://raw-ms2-data-bgc/
