# MS2 - Gestión de Cuentas

Microservicio para gestionar cuentas bancarias.

## 🏗️ Arquitectura

- **Lenguaje**: Node.js 18
- **Framework**: Express
- **Base de Datos**: MySQL 8.0
- **Puerto API**: 8002
- **Puerto DB**: 3306

## 📊 Estructura de Base de Datos

### Tabla: `tipos_cuenta`
- `tipo_cuenta_id` (PK, AUTO_INCREMENT)
- `nombre` (VARCHAR, UNIQUE)
- `descripcion` (TEXT)
- `costo_mantenimiento` (DECIMAL)
- `tasa_interes` (DECIMAL)
- `estado` (VARCHAR)

### Tabla: `cuentas`
- `cuenta_id` (PK, AUTO_INCREMENT)
- `cliente_id` (INT) → Referencia a MS1
- `tipo_cuenta_id` (FK → tipos_cuenta)
- `numero_cuenta` (VARCHAR, UNIQUE)
- `saldo` (DECIMAL)
- `moneda` (VARCHAR)
- `fecha_apertura` (TIMESTAMP)
- `estado` (VARCHAR)

## 🚀 Despliegue en EC2

### 1. Lanzar instancia EC2
```bash
# AMI: Ubuntu Server 22.04 LTS
# Tipo: t2.small (mínimo)
# Security Group: Permitir puertos 22, 8002, 3306
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
cd cloud-bank-service/ms2

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 📝 API Endpoints

### Health Check
```bash
GET http://<EC2-IP>:8002/
GET http://<EC2-IP>:8002/health
```

### Tipos de Cuenta

**Listar Tipos de Cuenta**
```bash
GET http://<EC2-IP>:8002/tipos-cuenta
```

**Obtener Tipo de Cuenta por ID**
```bash
GET http://<EC2-IP>:8002/tipos-cuenta/1
```

### Cuentas

**Crear Cuenta**
```bash
POST http://<EC2-IP>:8002/cuentas
Content-Type: application/json

{
  "cliente_id": 1,
  "tipo_cuenta_id": 1,
  "saldo": 1000.00,
  "moneda": "PEN"
}
```

**Listar Todas las Cuentas**
```bash
GET http://<EC2-IP>:8002/cuentas
```

**Obtener Cuenta por ID**
```bash
GET http://<EC2-IP>:8002/cuentas/1
```

**Obtener Cuentas por Cliente**
```bash
GET http://<EC2-IP>:8002/cuentas/cliente/1
```

**Obtener Cuenta por Número**
```bash
GET http://<EC2-IP>:8002/cuentas/numero/1001234567890
```

**Actualizar Saldo (Depósito/Retiro)**
```bash
PATCH http://<EC2-IP>:8002/cuentas/1/saldo
Content-Type: application/json

{
  "monto": 500.00,
  "operacion": "deposito"
}

# o para retiro:
{
  "monto": 200.00,
  "operacion": "retiro"
}
```

**Actualizar Estado de Cuenta**
```bash
PATCH http://<EC2-IP>:8002/cuentas/1/estado
Content-Type: application/json

{
  "estado": "bloqueada"
}
```

**Eliminar Cuenta**
```bash
DELETE http://<EC2-IP>:8002/cuentas/1
```

## 🧪 Pruebas Locales

```bash
# Levantar servicios
docker-compose up -d

# Probar API
curl http://localhost:8002/
curl http://localhost:8002/cuentas

# Ver logs
docker-compose logs -f api-cuentas

# Detener servicios
docker-compose down
```

## 🐳 Docker Hub

### Build y Push
```bash
cd api
docker build -t br4yangc/cloud-bank-ms2:api-cuentas .
docker push br4yangc/cloud-bank-ms2:api-cuentas
```

## 🔧 Variables de Entorno

- `DB_HOST`: mysql-db
- `DB_PORT`: 3306
- `DB_USER`: admin
- `DB_PASSWORD`: admin123
- `DB_NAME`: cuentas_db
- `PORT`: 8002

## 📦 Dependencias Node.js

- express: ^4.18.2
- mysql2: ^3.6.5
- cors: ^2.8.5
- dotenv: ^16.3.1
