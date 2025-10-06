# MS3 - Servicio de Perfil Completo del Cliente (Vista 360°)

## Descripción
Microservicio sin base de datos que agrega información completa de un cliente específico desde MS1 (PostgreSQL), MS2 (MySQL) y MS4 (MongoDB), presentándola de forma unificada para empleados del banco.

## Características
- ✅ **Stateless**: No tiene base de datos propia
- 🔄 **Agregador**: Consume datos de MS1, MS2 y MS4
- 🎯 **Vista 360°**: Información completa del cliente en un solo lugar
- 🚀 **FastAPI**: API REST moderna y rápida
- 🐳 **Dockerizado**: Listo para desplegar en EC2

## Tecnologías
- **Python 3.11**
- **FastAPI** - Framework web
- **httpx** - Cliente HTTP asíncrono
- **Pydantic** - Validación de datos
- **uvicorn** - Servidor ASGI

## Endpoints

### 1. Perfil Completo del Cliente
```http
GET /api/clientes/{cliente_id}/perfil-completo
```
Devuelve:
- Información personal (MS1)
- Todas las cuentas (MS2)
- Historial de transacciones (MS4)
- Resumen financiero calculado

### 2. Buscar Clientes
```http
GET /api/clientes/buscar?q=Juan
```
Busca clientes por nombre, email o documento.

### 3. Health Check
```http
GET /health
```
Verifica el estado del servicio y la conectividad con otros microservicios.

## Variables de Entorno

```env
# URLs de otros microservicios
MS1_URL=http://18.212.214.255:5000
MS2_URL=http://54.242.189.131:3000
MS4_URL=http://54.87.40.69:8080

# Configuración del servidor
PORT=6000
LOG_LEVEL=INFO
```

## Ejecución Local

### Con Docker
```bash
docker-compose up -d
```

### Sin Docker
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export MS1_URL=http://localhost:5000
export MS2_URL=http://localhost:3000
export MS4_URL=http://localhost:8080

# Ejecutar
python api/main.py
```

## Despliegue en EC2

```bash
# 1. Clonar repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service/ms3

# 2. Configurar variables de entorno
nano .env

# 3. Levantar contenedor
docker-compose up -d

# 4. Verificar logs
docker-compose logs -f

# 5. Probar endpoint
curl http://localhost:6000/health
```

## Arquitectura

```
┌─────────────────────────────────────────┐
│              MS3 API                    │
│         (FastAPI - Puerto 6000)         │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   Endpoint: perfil-completo       │ │
│  └───────────────────────────────────┘ │
│             ↓  ↓  ↓                     │
│      ┌──────┴──┴──┴──────┐             │
│      │  HTTP Clients     │             │
│      │  (httpx async)    │             │
│      └──────┬──┬──┬──────┘             │
└─────────────┼──┼──┼────────────────────┘
              │  │  │
    ┌─────────┘  │  └─────────┐
    ↓            ↓             ↓
  MS1 API     MS2 API      MS4 API
(PostgreSQL)  (MySQL)     (MongoDB)
```

## Ejemplo de Respuesta

```json
{
  "cliente": {
    "cliente_id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@example.com",
    "telefono": "+51999888777",
    "fecha_registro": "2024-01-15T10:30:00",
    "estado": "activo",
    "documento": {
      "tipo": "DNI",
      "numero": "12345678"
    }
  },
  "cuentas": [
    {
      "cuenta_id": 3,
      "numero_cuenta": "1234567890",
      "tipo_cuenta": "Cuenta de Ahorro",
      "saldo": 15000.00,
      "moneda": "PEN",
      "fecha_apertura": "2024-01-20",
      "estado": "activa"
    }
  ],
  "transacciones_recientes": [
    {
      "transaccionId": 45,
      "tipo": "DEPOSITO",
      "monto": 500.00,
      "fecha": "2024-10-05T10:30:00",
      "estado": "completada",
      "descripcion": "Depósito en efectivo"
    }
  ],
  "resumen_financiero": {
    "patrimonio_total": 15000.00,
    "moneda": "PEN",
    "total_cuentas": 1,
    "total_transacciones": 8,
    "ultima_actividad": "2024-10-05T10:30:00"
  }
}
```

## Mantenimiento

### Ver logs
```bash
docker-compose logs -f
```

### Reiniciar servicio
```bash
docker-compose restart
```

### Actualizar código
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

## Notas
- ⚠️ Este servicio depende de MS1, MS2 y MS4. Asegúrate de que estén corriendo.
- ⏱️ Los tiempos de respuesta dependen de la velocidad de los otros microservicios.
- 🔒 En producción, considera agregar autenticación/autorización.
