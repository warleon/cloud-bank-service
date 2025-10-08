# MS3 - Vista 360° del Cliente (Perfil Completo)

## 📋 Descripción

Microservicio agregador **sin base de datos propia** que integra información de múltiples microservicios (MS1, MS2, MS4) para proporcionar una vista completa y unificada del perfil de un cliente bancario. Diseñado para empleados del banco que necesitan acceso rápido a toda la información del cliente.

## 🎯 Propósito

- Proporcionar vista 360° del cliente en una sola llamada API
- Agregar datos de clientes, cuentas y transacciones
- Servir como Backend for Frontend (BFF) para aplicaciones internas
- Optimizar consultas evitando múltiples llamadas desde el frontend

## 🏗️ Arquitectura

```mermaid
graph TB
    subgraph "MS3 - Vista 360°"
        API[FastAPI Application]
        AGG[Aggregation Logic]
        
        API --> AGG
    end
    
    Client[Cliente Web/Móvil] -->|HTTP REST| API
    
    AGG -->|GET /clientes/{id}| MS1[MS1 - Clientes]
    AGG -->|GET /cuentas/cliente/{id}| MS2[MS2 - Cuentas]
    AGG -->|GET /transacciones/cuenta/{id}| MS4[MS4 - Transacciones]
    
    MS1 -->|Datos Cliente + Documentos| AGG
    MS2 -->|Cuentas + Tipos| AGG
    MS4 -->|Transacciones| AGG
    
    AGG -->|Respuesta Agregada| API
    
    style API fill:#9b59b6,color:#fff
    style AGG fill:#8e44ad,color:#fff
```

## 🛠️ Tecnologías

| Componente | Tecnología | Versión |
|------------|------------|---------|
| **Lenguaje** | Python | 3.11 |
| **Framework** | FastAPI | 0.104.1 |
| **Cliente HTTP** | httpx | 0.25.1 |
| **Servidor** | Uvicorn | 0.24.0 |
| **Validación** | Pydantic | 2.5.0 |
| **Contenedor** | Docker | - |

## 🌐 API Endpoints

### Perfil del Cliente

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/clientes/{cliente_id}/perfil-completo` | Vista 360° con toda la información del cliente |
| `GET` | `/api/clientes/buscar?q={query}` | Buscar clientes por nombre, email o documento |

### Utilidades

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información del servicio |
| `GET` | `/health` | Health check con estado de MS1, MS2, MS4 |
| `GET` | `/docs` | Documentación Swagger UI |

## 📊 Modelo de Respuesta Agregada

### Perfil Completo del Cliente
```json
{
  "cliente": {
    "cliente_id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@example.com",
    "telefono": "+51999888777",
    "estado": "activo",
    "documentos": [
      {
        "tipo_documento": "DNI",
        "numero_documento": "12345678"
      }
    ]
  },
  "cuentas": [
    {
      "cuenta_id": 1,
      "numero_cuenta": "1234567890",
      "tipo_cuenta": "Cuenta de Ahorros",
      "saldo": 15000.50,
      "moneda": "USD",
      "estado": "activa"
    }
  ],
  "transacciones_recientes": [
    {
      "transaccion_id": "...",
      "tipo": "transferencia",
      "monto": 500.00,
      "fecha": "2025-01-15T14:30:00"
    }
  ],
  "resumen": {
    "total_cuentas": 2,
    "saldo_total": 25000.50,
    "ultima_transaccion": "2025-01-15T14:30:00"
  }
}
```

## 📊 Estructura de Datos

**Sin Base de Datos Propia**
- Este microservicio NO tiene base de datos
- Consume datos en tiempo real de otros microservicios
- Caché opcional puede agregarse para optimización futura

**Fuentes de Datos:**
1. **MS1 (PostgreSQL)**: Datos del cliente y documentos
2. **MS2 (MySQL)**: Cuentas y tipos de cuenta
3. **MS4 (MongoDB)**: Transacciones bancarias

## ☁️ Servicios AWS Utilizados

- **EC2**: Hospedaje del contenedor
- **VPC & Security Groups**: Red y firewall (comunicación con MS1, MS2, MS4)
- **IAM**: Gestión de permisos

## 🚀 Despliegue Rápido

```bash
# En la instancia EC2
cd ~/cloud-bank-service/ms3

# Configurar IPs de otros microservicios en .env
# MS1_URL=http://54.167.116.254:8001
# MS2_URL=http://54.242.68.197:8002
# MS4_URL=http://52.90.2.132:8004

docker-compose up -d

# Verificar
curl http://localhost:6000/health
curl http://localhost:6000/docs
```

Ver guía completa: `../docs/DEPLOYMENT_GUIDE.md`

## 🔗 Dependencias

**Consumido por:**
- Frontend React (AWS Amplify)
- Aplicaciones internas del banco

**Consume:**
- MS1 (Clientes)
- MS2 (Cuentas)
- MS4 (Transacciones)

## 📖 Documentación Adicional

- **Swagger UI**: `http://{EC2-IP}:6000/docs`
- **OpenAPI Spec**: `http://{EC2-IP}:6000/openapi.json`
- **Integración con Frontend**: Ver `../frontend/README.md`
- **Guía de deployment detallada**: Ver `../docs/DEPLOYMENT_GUIDE.md`

## 📝 Notas

- **Stateless**: No mantiene estado, ideal para escalamiento horizontal
- **Resiliencia**: Si un MS falla, devuelve datos parciales con campo `error`
- **Health Check**: Muestra estado de conectividad con MS1, MS2, MS4
- **Timeout**: 10 segundos por llamada a cada microservicio
- **CORS**: Configurado para aceptar requests del frontend en Amplify
