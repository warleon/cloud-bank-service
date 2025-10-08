# Script de Validación de APIs - Cloud Bank Service
# Ejecutar en PowerShell

Write-Host "`n🔍 VALIDACIÓN DE APIS - Cloud Bank Service" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$apis = @(
    @{Name="MS1 (Clientes)"; URL="http://34.201.99.218:8001/health"},
    @{Name="MS2 (Cuentas)"; URL="http://13.222.184.86:8002/health"},
    @{Name="MS3 (Agregador)"; URL="http://98.88.19.214:6000/health"},
    @{Name="MS4 (Transacciones)"; URL="http://3.90.218.198:8004/health"},
    @{Name="MS5 (Analytics)"; URL="http://3.95.211.15:8000/health"}
)

Write-Host "Probando conectividad HTTP...`n" -ForegroundColor Yellow

foreach ($api in $apis) {
    try {
        $response = Invoke-WebRequest -Uri $api.URL -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($api.Name) - OK (HTTP 200)" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $($api.Name) - HTTP $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($api.Name) - FAIL" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Validación completada`n" -ForegroundColor Cyan

# Probar endpoints específicos
Write-Host "`nProbando endpoints de datos...`n" -ForegroundColor Yellow

$dataEndpoints = @(
    @{Name="MS1 - Clientes"; URL="http://34.201.99.218:8001/clientes"},
    @{Name="MS2 - Cuentas"; URL="http://13.222.184.86:8002/cuentas"},
    @{Name="MS4 - Transacciones"; URL="http://3.90.218.198:8004/transacciones"}
)

foreach ($endpoint in $dataEndpoints) {
    try {
        $response = Invoke-RestMethod -Uri $endpoint.URL -TimeoutSec 10
        $count = ($response | Measure-Object).Count
        Write-Host "✅ $($endpoint.Name) - $count registros" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($endpoint.Name) - FAIL" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ Todas las validaciones completadas`n" -ForegroundColor Green
