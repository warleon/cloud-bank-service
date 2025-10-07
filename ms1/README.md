# MS1 - Gestión de Clientes

## 📋 Descripción

Microservicio para la gestión completa de clientes bancarios y sus documentos de identidad. Proporciona operaciones CRUD sobre clientes y permite la asociación de múltiples documentos de identidad por cliente.

## 🎯 Propósito

- Centralizar la información de clientes del banco
- Gestionar datos personales y documentos de identidad
- Proporcionar API REST para otros microservicios
- Mantener integridad referencial con documentos asociados

## 🏗️ Arquitectura

```mermaid
graph TB
    subgraph "MS1 - Clientes"
        API[FastAPI Application]
        DB[(PostgreSQL)]
        
        API -->|SQLAlchemy ORM| DB
    end
    
    Client[Cliente Externo] -->|HTTP REST| API
    MS3[MS3 - Perfil 360°] -->|HTTP REST| API
    
    subgraph "Base de Datos"
        T1[Tabla: clientes]
        T2[Tabla: documentos_identidad]
        T1 -->|1:N| T2
    end
    
    DB --> T1
    DB --> T2
```

## 🛠️ Tecnologías

| Componente | Tecnología | Versión |
|------------|------------|---------|
| **Lenguaje** | Python | 3.11 |
| **Framework** | FastAPI | 0.104.1 |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Base de Datos** | PostgreSQL | 15 |
| **Servidor** | Uvicorn | 0.24.0 |
| **Validación** | Pydantic | 2.5.0 |
| **Contenedor** | Docker | - |

## 📊 Estructura de Base de Datos

### Tabla: `clientes`
- `cliente_id` (PK, SERIAL)
- `nombre` (VARCHAR)
- `apellido` (VARCHAR)
- `email` (VARCHAR, UNIQUE)
- `telefono` (VARCHAR)
- `fecha_registro` (TIMESTAMP)
- `estado` (VARCHAR)

### Tabla: `documentos_identidad`
- `documento_id` (PK, SERIAL)
- `cliente_id` (FK → clientes)
- `tipo_documento` (VARCHAR)
- `numero_documento` (VARCHAR, UNIQUE)
- `fecha_emision` (DATE)
- `fecha_vencimiento` (DATE)

## 🚀 Despliegue en EC2

### 1. Lanzar instancia EC2
```bash
# AMI: Ubuntu Server 22.04 LTS
# Tipo: t2.small (mínimo)
# Security Group: Permitir puertos 22, 8001, 5432
```

### 2. Conectar a EC2 e instalar Docker
```bash
ssh -i tu-key.pem ubuntu@<EC2-IP>

# Instalar Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# Cerrar sesión y volver a conectar
exit
ssh -i tu-key.pem ubuntu@<EC2-IP>
```

### 3. Clonar repositorio y desplegar
```bash
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service/ms1

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 📝 API Endpoints

### Health Check
```bash
GET http://<EC2-IP>:8001/
GET http://<EC2-IP>:8001/health
```

### Clientes

**Crear Cliente**
```bash
POST http://<EC2-IP>:8001/clientes
Content-Type: application/json

{
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
}
```

**Listar Clientes**
```bash
GET http://<EC2-IP>:8001/clientes
```

**Obtener Cliente por ID**
```bash
GET http://<EC2-IP>:8001/clientes/1
```

**Obtener Cliente por Email**
```bash
GET http://<EC2-IP>:8001/clientes/email/juan.perez@email.com
```

**Obtener Cliente por Documento**
```bash
GET http://<EC2-IP>:8001/clientes/documento/12345678
```

**Actualizar Cliente**
```bash
PUT http://<EC2-IP>:8001/clientes/1
Content-Type: application/json

{
  "nombre": "Juan Carlos",
  "apellido": "Pérez",
  "email": "juan.perez@email.com",
  "telefono": "999888777",
  "estado": "activo"
}
```

**Eliminar Cliente**
```bash
DELETE http://<EC2-IP>:8001/clientes/1
```

## 🧪 Pruebas Locales

```bash
# Levantar servicios
docker-compose up -d

# Probar API
curl http://localhost:8001/
curl http://localhost:8001/clientes

# Ver logs
docker-compose logs -f api-clientes

# Detener servicios
docker-compose down
```

## 🐳 Docker Hub

### Build y Push
```bash
cd api
docker build -t br4yangc/cloud-bank-ms1:api-clientes .
docker push br4yangc/cloud-bank-ms1:api-clientes
```

## 🔧 Variables de Entorno

- `DATABASE_URL`: postgresql://admin:admin123@postgres-db:5432/clientes_db
- `PORT`: 8001

## 📦 Dependencias Python

- fastapi==0.104.1
- uvicorn==0.24.0
- psycopg2-binary==2.9.9
- sqlalchemy==2.0.23
- pydantic==2.5.0
- python-dotenv==1.0.0
