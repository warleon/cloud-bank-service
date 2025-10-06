# 🏦 Cloud Bank - API REST de Consultas Analíticas# API REST - Consultas Analíticas DataLake



API REST desplegada en **EC2 Ubuntu 22.04** desarrollada con **FastAPI** que ejecuta consultas SQL sobre **Amazon Athena**, exponiendo endpoints analíticos para consultar datos del DataLake bancario almacenados en S3 y catalogados con AWS Glue.API REST desplegada en **EC2 Ubuntu 22.04** desarrollada con **FastAPI** que ejecuta consultas SQL sobre **Amazon Athena**, exponiendo 15+ endpoints analíticos para consultar datos del DataLake almacenados en S3 y catalogados con AWS Glue.



## 🎯 Descripción del Componente## 🎯 Descripción del Componente



Esta API implementa la capa de **Business Intelligence** del sistema bancario Cloud Bank, proporcionando:Esta API implementa la capa de acceso al DataLake, proporcionando:



### **Funcionalidades Implementadas:**### **Funcionalidades Implementadas:**

- ✅ **15+ Endpoints RESTful** para análisis bancarios- ✅ **15+ Endpoints RESTful** para consultas analíticas

- ✅ **Integración con Amazon Athena** vía boto3 SDK- ✅ **Integración con Amazon Athena** vía boto3 SDK

- ✅ **Consultas SQL sobre AWS Glue Data Catalog** (5 tablas catalogadas)- ✅ **Consultas SQL sobre AWS Glue Data Catalog** (9 tablas catalogadas)

- ✅ **Datos de 3 microservicios unificados**:- ✅ **Datos de múltiples fuentes**: MySQL, PostgreSQL y MongoDB unificados

  - MS1 (PostgreSQL): Clientes y documentos de identidad- ✅ **Dashboard general** con métricas agregadas

  - MS2 (MySQL): Cuentas y tipos de cuenta- ✅ **Queries personalizadas** vía endpoint POST

  - MS4 (MongoDB): Transacciones- ✅ **Documentación interactiva** con Swagger UI

- ✅ **Dashboard ejecutivo** con métricas clave del banco- ✅ **Health checks** y monitoreo

- ✅ **Análisis de clientes VIP** con patrimonio significativo- ✅ **CORS configurado** para acceso desde clientes web

- ✅ **Actividad transaccional diaria** (últimos 30 días)- ✅ **Logging estructurado** con niveles configurables

- ✅ **Queries personalizadas** vía endpoint POST

- ✅ **Documentación interactiva** con Swagger UI## 🚀 Despliegue en AWS

- ✅ **Health checks** y monitoreo

- ✅ **CORS configurado** para acceso desde clientes web### Infraestructura AWS Implementada:

- ✅ **Logging estructurado** con niveles configurables

**Amazon Athena:**

---- Motor de consultas SQL serverless

- Database: `datalake_db` (AWS Glue Data Catalog)

## 🏗️ Arquitectura AWS Implementada- 9 tablas catalogadas: `ms1_users`, `ms1_orders`, `ms1_products`, `ms2_customers`, `ms2_invoices`, `ms2_payments`, `ms3_inventory`, `ms3_shipments`, `ms3_suppliers`

- Output location: S3 bucket para resultados de queries

### **Amazon Athena:**

- Motor de consultas SQL serverless**AWS Glue Data Catalog:**

- Database: `cloud_bank_db` (AWS Glue Data Catalog)- 3 Crawlers configurados y ejecutados

- 5 tablas catalogadas:- 9 tablas con esquemas inferidos automáticamente

  - `ms1_ms1_clientes`- Particiones por fecha reconocidas

  - `ms1_ms1_documentos_identidad`- Tipos de datos correctamente mapeados

  - `ms2_ms2_tipos_cuenta`

  - `ms2_ms2_cuentas`**EC2 Ubuntu 22.04:**

  - `ms4_ms4_transacciones`- API corriendo en contenedor Docker

- Output location: S3 bucket para resultados de queries- Puerto 8000 expuesto

- IAM Role: `LabRole` con permisos Athena, Glue y S3

### **AWS Glue Data Catalog:**- Security Group configurado con puerto 8000 abierto

- 3 Crawlers configurados:- Health check endpoint activo

  - `crawler-ms1-clientes` → S3: `raw-ms1-data-bgc`

  - `crawler-ms2-cuentas` → S3: `raw-ms2-data-bgc`**Contenedor Docker:**

  - `crawler-ms4-transacciones` → S3: `raw-ms4-data-bgc`- Imagen: Python 3.11 slim

- Esquemas inferidos automáticamente- Framework: FastAPI 0.104.1

- Particiones por fecha (`year`, `month`, `day`)- ASGI Server: Uvicorn

- Tipos de datos correctamente mapeados- Dependencies: boto3, python-dotenv

- Variables de entorno configuradas vía `.env`

### **Amazon S3 (DataLake):**

- 3 buckets separados:## 🏗️ Arquitectura

  - `raw-ms1-data-bgc`: Datos de clientes (PostgreSQL)

  - `raw-ms2-data-bgc`: Datos de cuentas (MySQL)```

  - `raw-ms4-data-bgc`: Datos de transacciones (MongoDB)Cliente (Postman/Browser/App)

- Formato: JSON Lines (.json)    ↓

- Particionado por fecha: `year=YYYY/month=MM/day=DD/`API REST (FastAPI - Puerto 8000)

    ↓

### **EC2 Ubuntu 22.04:**AthenaClient (boto3)

- API corriendo en contenedor Docker    ↓

- Puerto 8000 expuestoAmazon Athena

- IAM Role: `LabRole` con permisos Athena, Glue y S3    ↓

- Security Group configurado con puerto 8000 abiertoAWS Glue Data Catalog

- Health check endpoint activo    ↓

Amazon S3 (Datos en JSON Lines)

### **Contenedor Docker:**```

- Imagen: Python 3.11 slim

- Framework: FastAPI 0.104.1## � Componentes AWS Integrados

- ASGI Server: Uvicorn

- Dependencies: boto3, python-dotenv, pyathenaEsta API se integra con los siguientes componentes ya desplegados:

- Variables de entorno configuradas vía `.env`

- ✅ **Amazon S3**: 3 buckets con datos en JSON Lines (`raw-ms1-data-bgc`, `raw-ms2-data-bgc`, `raw-ms3-data-bgc`)

---- ✅ **AWS Glue Data Catalog**: Database `datalake_db` con 9 tablas catalogadas

- ✅ **Amazon Athena**: Motor SQL serverless configurado con workgroup `primary`

## 📊 Endpoints Disponibles- ✅ **EC2 Ubuntu 22.04**: Servidor con Docker, IAM Role `LabRole`, Security Group con puerto 8000 abierto

- ✅ **IAM Role**: `LabRole` con permisos S3, Glue y Athena

### **Health & Status**- ✅ **Docker Network**: Aislamiento de contenedores en EC2

| Método | Endpoint | Descripción |

|--------|----------|-------------|## ⚙️ Configuración

| GET | `/` | Información del servicio y endpoints disponibles |

| GET | `/health` | Health check con verificación de conexión Athena |### Variables de Entorno

| GET | `/docs` | Documentación interactiva Swagger UI |

| GET | `/redoc` | Documentación ReDoc |1. Copia el archivo de ejemplo:

```bash

### **Clientes (MS1 - PostgreSQL)**cp .env.example .env

| Método | Endpoint | Descripción |```

|--------|----------|-------------|

| GET | `/api/clientes/resumen` | Resumen total de clientes (activos/inactivos) |2. Configura las variables en `.env`:

| GET | `/api/clientes/lista?limit=50` | Lista de clientes con documentos |```bash

| GET | `/api/clientes/con-cuentas?limit=50` | Clientes con sus cuentas y patrimonio total |# AWS Configuration

AWS_DEFAULT_REGION=us-east-1

### **Cuentas (MS2 - MySQL)**AWS_ACCESS_KEY_ID=          # Opcional si usas IAM Role

| Método | Endpoint | Descripción |AWS_SECRET_ACCESS_KEY=      # Opcional si usas IAM Role

|--------|----------|-------------|AWS_SESSION_TOKEN=          # Opcional si usas IAM Role

| GET | `/api/cuentas/resumen` | Resumen financiero del banco |

| GET | `/api/cuentas/por-tipo` | Cuentas agrupadas por tipo con totales |# Athena Configuration

| GET | `/api/cuentas/top-saldos?limit=20` | Top cuentas con mayores saldos |ATHENA_DATABASE=datalake_raw

ATHENA_OUTPUT_LOCATION=s3://raw-ms1-data-bgc/athena-results/

### **Transacciones (MS4 - MongoDB)**ATHENA_WORKGROUP=primary

| Método | Endpoint | Descripción |

|--------|----------|-------------|# API Configuration

| GET | `/api/transacciones/resumen` | Estadísticas de transacciones |API_HOST=0.0.0.0

| GET | `/api/transacciones/por-tipo` | Transacciones agrupadas por tipo |API_PORT=8000

| GET | `/api/transacciones/por-estado` | Transacciones agrupadas por estado |API_RELOAD=false

| GET | `/api/transacciones/recientes?limit=50` | Transacciones más recientes |

| GET | `/api/transacciones/detalladas?limit=50` | Transacciones con info completa de clientes |# Logging

LOG_LEVEL=INFO

### **Análisis de Negocio**```

| Método | Endpoint | Descripción |

|--------|----------|-------------|**Nota**: Si tu EC2 tiene un IAM Role asignado (como LabInstanceProfile), no necesitas configurar las credenciales AWS manualmente.

| GET | `/api/analisis/clientes-vip?threshold=10000&limit=20` | Clientes VIP con patrimonio > umbral |

| GET | `/api/analisis/actividad-diaria` | Actividad transaccional últimos 30 días |## Endpoints Disponibles



### **Dashboard Ejecutivo**### Health Check

| Método | Endpoint | Descripción |- GET / - Informacion del servicio

|--------|----------|-------------|- GET /health - Health check con verificacion de Athena

| GET | `/api/dashboard` | Métricas clave para dashboard ejecutivo |

### Ventas (MySQL)

### **Queries Personalizadas**- GET /api/ventas/resumen - Resumen general de ventas

| Método | Endpoint | Descripción |- GET /api/ventas/por-usuario - Ventas agrupadas por usuario

|--------|----------|-------------|- GET /api/ventas/por-estado - Ventas por estado de orden

| POST | `/api/query/custom` | Ejecutar query SQL personalizada (solo SELECT) |

| GET | `/api/queries/list` | Listar todas las queries predefinidas |### Productos

- GET /api/productos/top?limit=10 - Top productos por valor de inventario

---

### Clientes B2B (PostgreSQL)

## 🔧 Configuración y Despliegue- GET /api/clientes/top?limit=10 - Top clientes por facturacion

- GET /api/facturas/estado - Estado de facturas y pagos

### **1. Conectar al EC2**

```bash### Inventario y Logistica (MongoDB)

# Via EC2 Instance Connect (desde AWS Console)- GET /api/inventario/bajo-stock?threshold=100 - Productos con stock bajo

```- GET /api/envios/estado - Resumen de estado de envios



### **2. Clonar/Actualizar Repositorio**### Dashboard

```bash- GET /api/dashboard - Metricas para dashboard ejecutivo

cd ~

git clone https://github.com/Br4yanGC/cloud-bank-service.git### Custom Query

# O si ya existe: cd cloud-bank-service && git pull- POST /api/query/custom - Ejecutar query SQL personalizada

```

### Metadata

### **3. Configurar Variables de Entorno**- GET /api/queries/list - Listar queries predefinidas disponibles

```bash

cd cloud-bank-service/ms5/api-consultas## 📚 Documentación Interactiva

cp .env.example .env

nano .envUna vez corriendo la API, accede a:

```- **Swagger UI**: `http://<IP-PUBLICA-EC2>:8000/docs` (interfaz interactiva para probar endpoints)

- **ReDoc**: `http://<IP-PUBLICA-EC2>:8000/redoc` (documentación alternativa)

Configurar:- **Health Check**: `http://<IP-PUBLICA-EC2>:8000/health`

```env

# AWS Configuration## 🚀 Despliegue Implementado

AWS_REGION=us-east-1

AWS_ATHENA_DATABASE=cloud_bank_db### Contenedor Docker

AWS_ATHENA_OUTPUT_LOCATION=s3://athena-results-cloud-bank-bgc/El servicio está desplegado como contenedor Docker en EC2:



# Logging```bash

LOG_LEVEL=INFO# Contenedor construido y desplegado

```Container: api-consultas-datalake

Image: Python 3.11 slim + FastAPI

### **4. Construir y Ejecutar el Contenedor**Status: Running

```bashPort Mapping: 8000:8000

# Construir imagenNetwork: Default bridge

docker-compose buildRestart Policy: always

```

# Ejecutar en background

docker-compose up -d### Configuración de Red

**Security Group configurado con**:

# Ver logs- Type: Custom TCP

docker-compose logs -f- Port: 8000

```- Source: 0.0.0.0/0 (acceso público)

- Description: API DataLake access

### **5. Verificar API**

```bash### Acceso al Servicio

# Health checkLa API está accesible en:

curl http://localhost:8000/health- **Swagger UI**: `http://<IP-PUBLICA-EC2>:8000/docs`

- **Health Check**: `http://<IP-PUBLICA-EC2>:8000/health`

# Endpoint raíz- **Dashboard**: `http://<IP-PUBLICA-EC2>:8000/api/dashboard`

curl http://localhost:8000/- **Endpoints**: `http://<IP-PUBLICA-EC2>:8000/api/*`



# Dashboard ejecutivo### Verificación de Estado

curl http://localhost:8000/api/dashboard

``````bash

# Ver contenedor corriendo

---docker ps | grep api-consultas-datalake



## 📝 Ejemplos de Uso# Ver logs en tiempo real

docker logs api-consultas-datalake -f

### **Resumen de Clientes**

```bash# Health check desde el servidor

curl http://IP_EC2:8000/api/clientes/resumencurl http://localhost:8000/health

```# Response: {"status":"healthy","athena_connection":"ok"}

```

**Respuesta:**

```json## 📦 Colección de Postman

{

  "success": true,Importa la colección lista para usar: [`DataLake_API_Postman_Collection.json`](./DataLake_API_Postman_Collection.json)

  "data": [

    {**En Postman**:

      "total_clientes": 5,1. File → Import

      "clientes_activos": 5,2. Seleccionar el archivo JSON

      "clientes_inactivos": 03. La colección aparecerá con 16+ requests preconfiguradas

    }

  ],## 💡 Ejemplos de Uso

  "rows_count": 1,

  "execution_time_ms": 1234### Health Check

}```bash

```curl http://localhost:8000/health

```

### **Resumen Financiero del Banco****Respuesta:**

```bash```json

curl http://IP_EC2:8000/api/cuentas/resumen{

```  "status": "healthy",

  "athena_connection": "ok",

**Respuesta:**  "timestamp": "2025-10-05T02:47:10"

```json}

{```

  "success": true,

  "data": [### Resumen de Ventas

    {```bash

      "total_cuentas": 5,curl http://localhost:8000/api/ventas/resumen

      "saldo_total_banco": 67500.00,```

      "saldo_promedio": 13500.00,

      "saldo_minimo": 5000.00,### Top 5 Clientes

      "saldo_maximo": 25000.00```bash

    }curl http://localhost:8000/api/clientes/top?limit=5

  ],```

  "rows_count": 1,

  "execution_time_ms": 1456### Dashboard Ejecutivo

}```bash

```curl http://localhost:8000/api/dashboard

```

### **Top Cuentas con Mayores Saldos**

```bash### Query Personalizada (POST)

curl "http://IP_EC2:8000/api/cuentas/top-saldos?limit=3"```bash

```curl -X POST http://localhost:8000/api/query/custom \

  -H "Content-Type: application/json" \

**Respuesta:**  -d '{

```json    "query": "SELECT * FROM mysql_ms1_orders WHERE total_amount > 500 LIMIT 10"

{  }'

  "success": true,```

  "data": [

    {## 🛠️ Estructura del Proyecto

      "numero_cuenta": "1234567890",

      "nombre": "Juan",```

      "apellido": "Pérez",api-consultas/

      "email": "juan@example.com",├── main.py                    # Aplicación FastAPI con endpoints

      "saldo": 25000.00,├── athena_client.py           # Cliente para ejecutar queries en Athena

      "tipo_cuenta": "Ahorros Premium",├── queries.py                 # Queries SQL predefinidas

      "fecha_apertura": "2024-01-15"├── requirements.txt           # Dependencias Python

    },├── Dockerfile                 # Imagen Docker

    ...├── docker-compose.yml         # Orquestación del contenedor

  ],├── .env                       # Variables de entorno (no se sube a Git)

  "rows_count": 3,├── .env.example               # Plantilla de variables

  "execution_time_ms": 1678└── DataLake_API_Postman_Collection.json  # Colección de Postman

}```

```

## 🔧 Comandos Útiles

### **Transacciones Detalladas**

```bash### Ver logs

curl "http://IP_EC2:8000/api/transacciones/detalladas?limit=5"```bash

```docker logs api-consultas-datalake -f

```

**Respuesta:**

```json### Reiniciar contenedor

{```bash

  "success": true,docker-compose restart

  "data": [```

    {

      "transaccionid": "67890abcdef",### Detener contenedor

      "tipo": "TRANSFERENCIA",```bash

      "monto": 1500.00,docker-compose down

      "fecha": "2025-10-05T14:30:00",```

      "estado": "COMPLETADA",

      "descripcion": "Pago servicios",### Reconstruir después de cambios

      "cuenta_origen": "1234567890",```bash

      "cuenta_destino": "0987654321",docker-compose up -d --build

      "cliente_origen_nombre": "Juan",```

      "cliente_origen_apellido": "Pérez",

      "cliente_destino_nombre": "María",### Entrar al contenedor

      "cliente_destino_apellido": "González"```bash

    },docker exec -it api-consultas-datalake bash

    ...```

  ],

  "rows_count": 5,## 🐛 Troubleshooting

  "execution_time_ms": 2345

}### Error: "Connection to Athena failed"

```**Causa**: IAM Role sin permisos o región incorrecta

**Solución**:

### **Dashboard Ejecutivo**```bash

```bash# Verificar IAM Role del EC2

curl http://IP_EC2:8000/api/dashboardaws sts get-caller-identity

```

# Verificar región en .env

**Respuesta:**cat .env | grep AWS_DEFAULT_REGION

```json```

{

  "success": true,### Error: "Table not found"

  "data": [**Causa**: Glue Crawlers no han ejecutado o tabla no existe

    {"metrica": "Total Clientes", "valor": "5", "categoria": "clientes"},**Solución**:

    {"metrica": "Total Cuentas", "valor": "5", "categoria": "cuentas"},```bash

    {"metrica": "Saldo Total Banco", "valor": "67500.00", "categoria": "cuentas"},# Listar tablas disponibles

    {"metrica": "Total Transacciones", "valor": "6", "categoria": "transacciones"},curl http://localhost:8000/api/tablas

    {"metrica": "Volumen Transaccional", "valor": "15000.00", "categoria": "transacciones"},```

    {"metrica": "Clientes Activos", "valor": "5", "categoria": "clientes"}

  ],### Error: "Port 8000 already in use"

  "rows_count": 6,**Causa**: Otro servicio usa el puerto 8000

  "execution_time_ms": 2890**Solución**:

}```bash

```# Cambiar puerto en .env

API_PORT=8001

### **Clientes VIP**

```bash# O detener el servicio que usa el puerto

curl "http://IP_EC2:8000/api/analisis/clientes-vip?threshold=15000&limit=10"sudo lsof -i :8000

``````



### **Query Personalizada (POST)**### No puedo acceder desde mi navegador

```bash**Causa**: Puerto 8000 no está abierto en Security Group

curl -X POST http://IP_EC2:8000/api/query/custom \**Solución**: Ver paso 3 de "Instalación y Ejecución"

  -H "Content-Type: application/json" \

  -d '{## 📊 Detalles de los Endpoints

    "query": "SELECT tipo, COUNT(*) as total FROM cloud_bank_db.ms4_ms4_transacciones GROUP BY tipo",

    "database": "cloud_bank_db"### Endpoints de Solo Lectura (GET)

  }'

```| Endpoint | Descripción | Parámetros |

|----------|-------------|------------|

---| `/` | Información del servicio | - |

| `/health` | Health check con verificación Athena | - |

## 🔐 Seguridad| `/api/dashboard` | Dashboard con métricas generales | - |

| `/api/ventas/resumen` | Resumen total de ventas | - |

- ✅ **IAM Role** con permisos mínimos necesarios| `/api/ventas/por-usuario` | Ventas agrupadas por usuario | - |

- ✅ **Security Group** con reglas específicas| `/api/clientes/top` | Top clientes por facturación | `limit` (default: 10) |

- ✅ **Validación de queries** (solo SELECT permitido)| `/api/productos/mas-vendidos` | Productos más vendidos | `limit` (default: 10) |

- ✅ **Sanitización de inputs** para prevenir SQL injection| `/api/inventario/estado` | Estado del inventario | - |

- ✅ **CORS** configurado correctamente| `/api/inventario/bajo-stock` | Productos con stock bajo | `threshold` (default: 50) |

- ✅ **Logging** de todas las peticiones| `/api/pagos/estado` | Resumen de pagos por estado | - |

| `/api/facturas/pendientes` | Facturas con estado pending | - |

---| `/api/envios/por-estado` | Envíos agrupados por estado | - |

| `/api/proveedores/activos` | Proveedores activos | - |

## 📈 Monitoreo| `/api/ordenes/alto-valor` | Órdenes de alto valor | `min_amount` (default: 500) |

| `/api/tablas` | Lista tablas disponibles en Glue | - |

### **Logs del Contenedor**

```bash### Endpoints de Escritura (POST)

docker-compose logs -f

```| Endpoint | Descripción | Body |

|----------|-------------|------|

### **Estado del Contenedor**| `/api/query/custom` | Ejecutar query SQL personalizada | `{"query": "SELECT * FROM ..."}` |

```bash

docker-compose ps## 🔐 Seguridad

```

### Variables de Entorno

### **Reiniciar el Servicio**- ✅ Las credenciales AWS se obtienen del IAM Role (no hardcoded)

```bash- ✅ Archivo `.env` no se sube a Git (protegido por `.gitignore`)

docker-compose restart- ✅ `.env.example` es solo una plantilla sin credenciales reales

```

### CORS

---- ⚠️ Actualmente permite todos los orígenes (`allow_origins=["*"]`)

- 📝 En producción, especifica dominios permitidos

## 🧪 Testing

### Rate Limiting

### **Health Check**- ⚠️ No implementado actualmente

```bash- 📝 Considera agregar rate limiting en producción

curl http://localhost:8000/health

```## 📈 Performance y Costos



### **Documentación Interactiva**### Tiempos de Respuesta Observados

Abrir en navegador:- Health check: < 100ms

```- Queries simples (SELECT * FROM tabla LIMIT 10): 2-5 segundos

http://IP_EC2:8000/docs- Queries complejas (agregaciones, filtros): 5-15 segundos

```- Dashboard general: 8-12 segundos (múltiples queries)



---### Optimización Implementada

- ✅ Particionamiento por fecha en S3 reduce datos escaneados

## 🚀 Próximos Pasos- ✅ Uso de `LIMIT` en queries para resultados acotados

- ✅ Formato JSON Lines optimizado para Athena

1. ✅ **API REST funcionando** con 15+ endpoints- ✅ IAM Role en EC2 elimina overhead de credenciales temporales

2. ⏳ **Configurar API Gateway** para HTTPS (opcional)

3. ⏳ **Implementar autenticación** JWT/OAuth (opcional)### Costos AWS Athena

4. ⏳ **Agregar rate limiting** (opcional)- Precio: $5 USD por TB de datos escaneados

5. ⏳ **Métricas con CloudWatch** (opcional)- Con particionamiento y datos de prueba: costo mínimo (< $0.01 por query)

- Sin particiones: Athena escanea todo el bucket

---

## 🔍 Estado de Implementación

## 📚 Tecnologías Utilizadas

### ✅ Completado

- **FastAPI** 0.104.1 - Framework web- 15+ endpoints analíticos funcionando

- **Uvicorn** - ASGI server- Integración con Athena operativa

- **Boto3** - AWS SDK para Python- Datos de 3 fuentes unificados

- **PyAthena** - Cliente Athena- Documentación Swagger UI activa

- **Pydantic** - Validación de datos- Health checks implementados

- **Python** 3.11- CORS configurado

- **Docker** - Containerización- Logging estructurado

- **Amazon Athena** - Motor de consultas- Colección Postman con 16 requests

- **AWS Glue** - Data Catalog- Despliegue en EC2 con Docker

- **Amazon S3** - DataLake storage- IAM Role configurado



---### 📊 Métricas del Sistema

- **9 tablas** catalogadas en Glue

## 👨‍💻 Autor- **3 fuentes** de datos integradas

- **15+ endpoints** disponibles

**Cloud Bank Project** - Sistema Bancario Completo en AWS  - **Puerto 8000** expuesto

Módulo 5: DataLake & Analytics API- **JSON Lines** como formato de datos


## 📄 Información del Proyecto

Este componente es parte de un proyecto educativo para AWS Academy que implementa una arquitectura completa de DataLake en AWS, utilizando servicios como S3, Glue, Athena y EC2.