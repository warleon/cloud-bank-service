# Script para verificar bases de datos remotamente desde Windows
# Verificar estado de las bases de datos en cada microservicio

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "VERIFICACIÓN REMOTA DE BASES DE DATOS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Solicitar nuevas IPs si han cambiado
Write-Host "Ingresa las nuevas IPs públicas de tus instancias EC2:" -ForegroundColor Yellow
$MS1_IP = Read-Host "IP de MS1 (PostgreSQL)"
$MS2_IP = Read-Host "IP de MS2 (MySQL)"
$MS4_IP = Read-Host "IP de MS4 (MongoDB)"
$MS5_IP = Read-Host "IP de MS5 (DataLake)"
Write-Host ""

# MS1 - PostgreSQL
Write-Host "[MS1] Verificando PostgreSQL en $MS1_IP..." -ForegroundColor Yellow
ssh ubuntu@$MS1_IP "PGPASSWORD=admin123 psql -h localhost -U admin -d clientes_db -t -c 'SELECT COUNT(*) as clientes FROM clientes; SELECT COUNT(*) as documentos FROM documentos_identidad;'"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MS1 PostgreSQL: CONECTADO" -ForegroundColor Green
} else {
    Write-Host "✗ MS1 PostgreSQL: ERROR" -ForegroundColor Red
}
Write-Host ""

# MS2 - MySQL
Write-Host "[MS2] Verificando MySQL en $MS2_IP..." -ForegroundColor Yellow
ssh ubuntu@$MS2_IP "mysql -h localhost -u admin -padmin123 -D cuentas_db -N -e 'SELECT COUNT(*) as cuentas FROM cuentas; SELECT COUNT(*) as tipos FROM tipos_cuenta;'"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MS2 MySQL: CONECTADO" -ForegroundColor Green
} else {
    Write-Host "✗ MS2 MySQL: ERROR" -ForegroundColor Red
}
Write-Host ""

# MS4 - MongoDB
Write-Host "[MS4] Verificando MongoDB en $MS4_IP..." -ForegroundColor Yellow
ssh ubuntu@$MS4_IP "mongosh mongodb://admin:admin123@localhost:27017/transacciones_db --authenticationDatabase admin --quiet --eval 'print(db.transacciones.countDocuments())'"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MS4 MongoDB: CONECTADO" -ForegroundColor Green
} else {
    Write-Host "✗ MS4 MongoDB: ERROR" -ForegroundColor Red
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "VERIFICACIÓN COMPLETA" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Preguntar si quiere actualizar las IPs en los archivos .env
Write-Host "¿Deseas actualizar las IPs en los archivos de configuración? (S/N)" -ForegroundColor Yellow
$update = Read-Host
if ($update -eq "S" -or $update -eq "s") {
    Write-Host "Actualizando IPs en archivos .env..." -ForegroundColor Cyan
    
    # Actualizar ms5/datalake-ingester/.env
    $envFile = "ms5\datalake-ingester\.env"
    (Get-Content $envFile) | ForEach-Object {
        $_ -replace 'POSTGRES_HOST=.*', "POSTGRES_HOST=$MS1_IP" `
           -replace 'MYSQL_HOST=.*', "MYSQL_HOST=$MS2_IP" `
           -replace 'MONGO_HOST=.*', "MONGO_HOST=$MS4_IP"
    } | Set-Content $envFile
    
    Write-Host "✓ Actualizado: $envFile" -ForegroundColor Green
    
    # Mostrar resumen
    Write-Host ""
    Write-Host "Nuevas IPs configuradas:" -ForegroundColor Cyan
    Write-Host "  MS1 (PostgreSQL): $MS1_IP" -ForegroundColor White
    Write-Host "  MS2 (MySQL):      $MS2_IP" -ForegroundColor White
    Write-Host "  MS4 (MongoDB):    $MS4_IP" -ForegroundColor White
    Write-Host "  MS5 (DataLake):   $MS5_IP" -ForegroundColor White
}
