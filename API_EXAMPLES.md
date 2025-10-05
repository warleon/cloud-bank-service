# 🧪 Ejemplos de Pruebas API - Cloud Bank

Colección de ejemplos para probar cada microservicio con curl o Postman.

---

## 🔧 Configuración Inicial

Reemplaza estas variables con tus IPs reales:

```bash
MS1_URL="http://<EC2-MS1-IP>:8001"
MS2_URL="http://<EC2-MS2-IP>:8002"
MS4_URL="http://<EC2-MS4-IP>:8004"
```

---

## 🔹 MS1 - Gestión de Clientes

### Health Check
```bash
curl $MS1_URL/
curl $MS1_URL/health
```

### Crear Cliente
```bash
curl -X POST $MS1_URL/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@email.com",
    "telefono": "999888777",
    "estado": "activo",
    "documento": {
      "tipo_documento": "DNI",
      "numero_documento": "12345678",
      "fecha_emision": "2020-01-15",
      "fecha_vencimiento": "2030-01-15"
    }
  }'
```

### Listar Clientes
```bash
curl $MS1_URL/clientes
```

### Obtener Cliente por ID
```bash
curl $MS1_URL/clientes/1
```

### Obtener Cliente por Email
```bash
curl $MS1_URL/clientes/email/juan.perez@email.com
```

### Obtener Cliente por Documento
```bash
curl $MS1_URL/clientes/documento/12345678
```

### Actualizar Cliente
```bash
curl -X PUT $MS1_URL/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Carlos",
    "apellido": "Pérez García",
    "email": "juan.perez@email.com",
    "telefono": "999888777",
    "estado": "activo"
  }'
```

### Eliminar Cliente
```bash
curl -X DELETE $MS1_URL/clientes/1
```

---

## 🔹 MS2 - Gestión de Cuentas

### Health Check
```bash
curl $MS2_URL/
curl $MS2_URL/health
```

### Listar Tipos de Cuenta
```bash
curl $MS2_URL/tipos-cuenta
```

### Obtener Tipo de Cuenta por ID
```bash
curl $MS2_URL/tipos-cuenta/1
```

### Crear Cuenta
```bash
curl -X POST $MS2_URL/cuentas \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "tipo_cuenta_id": 1,
    "saldo": 1000.00,
    "moneda": "PEN"
  }'
```

### Listar Todas las Cuentas
```bash
curl $MS2_URL/cuentas
```

### Obtener Cuenta por ID
```bash
curl $MS2_URL/cuentas/1
```

### Obtener Cuentas por Cliente
```bash
curl $MS2_URL/cuentas/cliente/1
```

### Obtener Cuenta por Número
```bash
curl $MS2_URL/cuentas/numero/1001234567890
```

### Realizar Depósito
```bash
curl -X PATCH $MS2_URL/cuentas/1/saldo \
  -H "Content-Type: application/json" \
  -d '{
    "monto": 500.00,
    "operacion": "deposito"
  }'
```

### Realizar Retiro
```bash
curl -X PATCH $MS2_URL/cuentas/1/saldo \
  -H "Content-Type: application/json" \
  -d '{
    "monto": 200.00,
    "operacion": "retiro"
  }'
```

### Actualizar Estado de Cuenta
```bash
curl -X PATCH $MS2_URL/cuentas/1/estado \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "bloqueada"
  }'
```

### Eliminar Cuenta
```bash
curl -X DELETE $MS2_URL/cuentas/1
```

---

## 🔹 MS4 - Gestión de Transacciones

### Health Check
```bash
curl $MS4_URL/
curl $MS4_URL/health
```

### Crear Depósito
```bash
curl -X POST $MS4_URL/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "DEPOSITO",
    "cuentaDestinoId": 1,
    "monto": 1000.00,
    "moneda": "PEN",
    "descripcion": "Depósito inicial",
    "metadata": {
      "canal": "CAJERO",
      "ubicacion": "Lima"
    }
  }'
```

### Crear Retiro
```bash
curl -X POST $MS4_URL/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "RETIRO",
    "cuentaOrigenId": 1,
    "monto": 200.00,
    "moneda": "PEN",
    "descripcion": "Retiro cajero automático"
  }'
```

### Crear Transferencia
```bash
curl -X POST $MS4_URL/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "TRANSFERENCIA",
    "cuentaOrigenId": 1,
    "cuentaDestinoId": 2,
    "monto": 500.00,
    "moneda": "PEN",
    "descripcion": "Transferencia entre cuentas"
  }'
```

### Crear Pago de Servicio
```bash
curl -X POST $MS4_URL/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "PAGO_SERVICIO",
    "cuentaOrigenId": 1,
    "monto": 150.50,
    "moneda": "PEN",
    "descripcion": "Pago de luz",
    "metadata": {
      "servicio": "LUZ_DEL_SUR",
      "recibo": "123456789"
    }
  }'
```

### Listar Transacciones
```bash
curl $MS4_URL/transacciones
```

### Obtener Transacción por ID
```bash
curl $MS4_URL/transacciones/507f1f77bcf86cd799439011
```

### Obtener Transacción por Transaction ID
```bash
curl $MS4_URL/transacciones/transaccion-id/TRX001
```

### Obtener Transacciones por Cuenta
```bash
curl $MS4_URL/transacciones/cuenta/1
```

### Obtener Transacciones por Tipo
```bash
# Tipos válidos: DEPOSITO, RETIRO, TRANSFERENCIA, PAGO_SERVICIO
curl $MS4_URL/transacciones/tipo/DEPOSITO
curl $MS4_URL/transacciones/tipo/TRANSFERENCIA
```

### Obtener Transacciones por Estado
```bash
# Estados válidos: PENDIENTE, COMPLETADA, FALLIDA, CANCELADA
curl $MS4_URL/transacciones/estado/COMPLETADA
curl $MS4_URL/transacciones/estado/PENDIENTE
```

### Obtener Transacciones por Rango de Fechas
```bash
curl "$MS4_URL/transacciones/fecha-rango?inicio=2024-01-01T00:00:00&fin=2024-12-31T23:59:59"
```

### Actualizar Estado de Transacción
```bash
curl -X PATCH $MS4_URL/transacciones/507f1f77bcf86cd799439011/estado \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "COMPLETADA"
  }'
```

### Eliminar Transacción
```bash
curl -X DELETE $MS4_URL/transacciones/507f1f77bcf86cd799439011
```

---

## 🔄 Flujo Completo de Ejemplo

### Escenario: Nuevo cliente realiza depósito

```bash
# 1. Crear cliente
curl -X POST $MS1_URL/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María",
    "apellido": "González",
    "email": "maria.gonzalez@email.com",
    "telefono": "987654321",
    "documento": {
      "tipo_documento": "DNI",
      "numero_documento": "87654321",
      "fecha_emision": "2021-01-01",
      "fecha_vencimiento": "2031-01-01"
    }
  }'

# Resultado: cliente_id = 4

# 2. Crear cuenta para el cliente
curl -X POST $MS2_URL/cuentas \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 4,
    "tipo_cuenta_id": 2,
    "saldo": 0,
    "moneda": "PEN"
  }'

# Resultado: cuenta_id = 5, numero_cuenta = 1004567890123

# 3. Realizar depósito inicial
curl -X POST $MS4_URL/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "DEPOSITO",
    "cuentaDestinoId": 5,
    "monto": 5000.00,
    "moneda": "PEN",
    "descripcion": "Depósito inicial de apertura"
  }'

# 4. Verificar saldo actualizado
curl $MS2_URL/cuentas/5

# 5. Ver historial de transacciones
curl $MS4_URL/transacciones/cuenta/5
```

---

## 📊 Casos de Prueba Avanzados

### Escenario 1: Transferencia entre cuentas

```bash
# Cuenta origen: ID 1
# Cuenta destino: ID 2

# Ver saldos antes
curl $MS2_URL/cuentas/1
curl $MS2_URL/cuentas/2

# Realizar transferencia
curl -X POST $MS4_URL/transacciones \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "TRANSFERENCIA",
    "cuentaOrigenId": 1,
    "cuentaDestinoId": 2,
    "monto": 1000.00,
    "moneda": "PEN",
    "descripcion": "Pago de servicios"
  }'

# Actualizar saldo cuenta origen (restar)
curl -X PATCH $MS2_URL/cuentas/1/saldo \
  -H "Content-Type: application/json" \
  -d '{"monto": 1000.00, "operacion": "retiro"}'

# Actualizar saldo cuenta destino (sumar)
curl -X PATCH $MS2_URL/cuentas/2/saldo \
  -H "Content-Type: application/json" \
  -d '{"monto": 1000.00, "operacion": "deposito"}'

# Ver saldos después
curl $MS2_URL/cuentas/1
curl $MS2_URL/cuentas/2
```

### Escenario 2: Cliente con múltiples cuentas

```bash
# Crear cuenta en soles
curl -X POST $MS2_URL/cuentas \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "tipo_cuenta_id": 1,
    "saldo": 5000,
    "moneda": "PEN"
  }'

# Crear cuenta en dólares
curl -X POST $MS2_URL/cuentas \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "tipo_cuenta_id": 4,
    "saldo": 1000,
    "moneda": "USD"
  }'

# Ver todas las cuentas del cliente
curl $MS2_URL/cuentas/cliente/1
```

### Escenario 3: Búsqueda y filtrado

```bash
# Buscar cliente por email
curl $MS1_URL/clientes/email/juan.perez@email.com

# Buscar transacciones por tipo
curl $MS4_URL/transacciones/tipo/DEPOSITO

# Filtrar transacciones por estado
curl $MS4_URL/transacciones/estado/COMPLETADA

# Buscar transacciones de una cuenta específica
curl $MS4_URL/transacciones/cuenta/1
```

---

## 🧪 Scripts de Prueba Automatizada

### Bash Script - Test MS1

```bash
#!/bin/bash
MS1_URL="http://localhost:8001"

echo "Testing MS1 - Clientes..."

# Health check
echo "1. Health check..."
curl -s $MS1_URL/health | jq

# Crear cliente
echo "2. Crear cliente..."
RESPONSE=$(curl -s -X POST $MS1_URL/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test",
    "apellido": "User",
    "email": "test@email.com",
    "telefono": "111222333",
    "documento": {
      "tipo_documento": "DNI",
      "numero_documento": "11122233",
      "fecha_emision": "2020-01-01",
      "fecha_vencimiento": "2030-01-01"
    }
  }')

echo $RESPONSE | jq
CLIENTE_ID=$(echo $RESPONSE | jq -r '.cliente_id')

# Listar clientes
echo "3. Listar clientes..."
curl -s $MS1_URL/clientes | jq

# Obtener cliente
echo "4. Obtener cliente $CLIENTE_ID..."
curl -s $MS1_URL/clientes/$CLIENTE_ID | jq

echo "✅ MS1 tests completed!"
```

### Python Script - Test completo

```python
import requests
import json

MS1_URL = "http://localhost:8001"
MS2_URL = "http://localhost:8002"
MS4_URL = "http://localhost:8004"

def test_complete_flow():
    print("🧪 Testing complete flow...")
    
    # 1. Crear cliente
    print("\n1️⃣ Creating client...")
    cliente_data = {
        "nombre": "Pedro",
        "apellido": "Ramírez",
        "email": "pedro.ramirez@test.com",
        "telefono": "999111222",
        "documento": {
            "tipo_documento": "DNI",
            "numero_documento": "99911122",
            "fecha_emision": "2021-01-01",
            "fecha_vencimiento": "2031-01-01"
        }
    }
    
    response = requests.post(f"{MS1_URL}/clientes", json=cliente_data)
    cliente = response.json()
    cliente_id = cliente['cliente_id']
    print(f"✅ Cliente creado: ID {cliente_id}")
    
    # 2. Crear cuenta
    print("\n2️⃣ Creating account...")
    cuenta_data = {
        "cliente_id": cliente_id,
        "tipo_cuenta_id": 1,
        "saldo": 1000,
        "moneda": "PEN"
    }
    
    response = requests.post(f"{MS2_URL}/cuentas", json=cuenta_data)
    cuenta = response.json()
    cuenta_id = cuenta['cuenta_id']
    print(f"✅ Cuenta creada: ID {cuenta_id}")
    
    # 3. Crear transacción
    print("\n3️⃣ Creating transaction...")
    transaccion_data = {
        "tipo": "DEPOSITO",
        "cuentaDestinoId": cuenta_id,
        "monto": 500,
        "moneda": "PEN",
        "descripcion": "Test deposit"
    }
    
    response = requests.post(f"{MS4_URL}/transacciones", json=transaccion_data)
    transaccion = response.json()
    print(f"✅ Transacción creada: {transaccion['transaccionId']}")
    
    print("\n🎉 Complete flow test passed!")

if __name__ == "__main__":
    test_complete_flow()
```

---

## 📝 Notas Importantes

### Códigos de Estado HTTP

- **200 OK**: Operación exitosa (GET, PUT, PATCH)
- **201 Created**: Recurso creado exitosamente (POST)
- **204 No Content**: Eliminación exitosa (DELETE)
- **400 Bad Request**: Datos inválidos
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

### Headers Importantes

Todas las APIs aceptan y retornan JSON:

```bash
-H "Content-Type: application/json"
-H "Accept: application/json"
```

### Formateo de Respuestas

Para ver respuestas formateadas con jq:

```bash
curl -s $MS1_URL/clientes | jq
```

---

## 🔍 Debugging

### Ver Headers de Respuesta

```bash
curl -i $MS1_URL/clientes
```

### Ver Request y Response Completos

```bash
curl -v $MS1_URL/clientes
```

### Timeout Personalizado

```bash
curl --max-time 10 $MS4_URL/transacciones
```

---

## 📦 Colección de Postman

Para importar en Postman, crea un JSON con esta estructura:

```json
{
  "info": {
    "name": "Cloud Bank APIs",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "ms1_url",
      "value": "http://localhost:8001"
    },
    {
      "key": "ms2_url",
      "value": "http://localhost:8002"
    },
    {
      "key": "ms4_url",
      "value": "http://localhost:8004"
    }
  ]
}
```

---

**¡Happy Testing! 🧪**
