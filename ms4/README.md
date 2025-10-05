# MS4 - Gestión de Transacciones

Microservicio para gestionar transacciones bancarias.

## 🏗️ Arquitectura

- **Lenguaje**: Java 17
- **Framework**: Spring Boot 3.2.1
- **Base de Datos**: MongoDB 7.0
- **Puerto API**: 8004
- **Puerto DB**: 27017

## 📊 Estructura de Base de Datos

### Colección: `transacciones`
```json
{
  "_id": ObjectId,
  "transaccionId": String (unique),
  "tipo": Enum ["DEPOSITO", "RETIRO", "TRANSFERENCIA", "PAGO_SERVICIO"],
  "cuentaOrigenId": Integer,
  "cuentaDestinoId": Integer,
  "monto": Double,
  "moneda": String ["PEN", "USD", "EUR"],
  "descripcion": String,
  "fecha": DateTime,
  "estado": Enum ["PENDIENTE", "COMPLETADA", "FALLIDA", "CANCELADA"],
  "metadata": Object
}
```

## 🚀 Despliegue en EC2

### 1. Lanzar instancia EC2
```bash
# AMI: Ubuntu Server 22.04 LTS
# Tipo: t2.medium (recomendado para Java)
# Security Group: Permitir puertos 22, 8004, 27017
# Storage: 20GB mínimo
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
cd cloud-bank-service/ms4

# Levantar servicios (build puede tomar 3-5 minutos)
docker-compose up -d

# Ver logs (esperar a que Spring Boot inicie)
docker-compose logs -f api-transacciones
```

**Nota**: La primera construcción de la imagen Java puede tomar varios minutos debido a la descarga de dependencias Maven.

## 📝 API Endpoints

### Health Check
```bash
GET http://<EC2-IP>:8004/
GET http://<EC2-IP>:8004/health
```

### Transacciones

**Crear Transacción**
```bash
POST http://<EC2-IP>:8004/transacciones
Content-Type: application/json

{
  "tipo": "DEPOSITO",
  "cuentaDestinoId": 1,
  "monto": 1000.00,
  "moneda": "PEN",
  "descripcion": "Depósito inicial",
  "metadata": {
    "canal": "WEB",
    "ubicacion": "Lima"
  }
}

# Transferencia
{
  "tipo": "TRANSFERENCIA",
  "cuentaOrigenId": 1,
  "cuentaDestinoId": 2,
  "monto": 500.00,
  "moneda": "PEN",
  "descripcion": "Transferencia entre cuentas"
}
```

**Listar Todas las Transacciones**
```bash
GET http://<EC2-IP>:8004/transacciones
```

**Obtener Transacción por ID**
```bash
GET http://<EC2-IP>:8004/transacciones/507f1f77bcf86cd799439011
```

**Obtener Transacción por Transaction ID**
```bash
GET http://<EC2-IP>:8004/transacciones/transaccion-id/TRX001
```

**Obtener Transacciones por Cuenta**
```bash
GET http://<EC2-IP>:8004/transacciones/cuenta/1
```

**Obtener Transacciones por Tipo**
```bash
GET http://<EC2-IP>:8004/transacciones/tipo/TRANSFERENCIA

# Tipos válidos: DEPOSITO, RETIRO, TRANSFERENCIA, PAGO_SERVICIO
```

**Obtener Transacciones por Estado**
```bash
GET http://<EC2-IP>:8004/transacciones/estado/COMPLETADA

# Estados válidos: PENDIENTE, COMPLETADA, FALLIDA, CANCELADA
```

**Obtener Transacciones por Rango de Fechas**
```bash
GET http://<EC2-IP>:8004/transacciones/fecha-rango?inicio=2024-01-01T00:00:00&fin=2024-12-31T23:59:59
```

**Actualizar Estado de Transacción**
```bash
PATCH http://<EC2-IP>:8004/transacciones/507f1f77bcf86cd799439011/estado
Content-Type: application/json

{
  "estado": "COMPLETADA"
}
```

**Eliminar Transacción**
```bash
DELETE http://<EC2-IP>:8004/transacciones/507f1f77bcf86cd799439011
```

## 🧪 Pruebas Locales

```bash
# Levantar servicios
docker-compose up -d

# Probar API (esperar ~2 minutos para que Spring Boot inicie)
curl http://localhost:8004/
curl http://localhost:8004/transacciones

# Ver logs
docker-compose logs -f api-transacciones

# Detener servicios
docker-compose down
```

## 🐳 Docker Hub

### Build y Push
```bash
cd api
docker build -t br4yangc/cloud-bank-ms4:api-transacciones .
docker push br4yangc/cloud-bank-ms4:api-transacciones
```

## 🔧 Variables de Entorno

- `SPRING_DATA_MONGODB_URI`: mongodb://admin:admin123@mongodb:27017/transacciones_db?authSource=admin
- `SERVER_PORT`: 8004

## 📦 Dependencias

- Spring Boot 3.2.1
- Spring Boot Starter Web
- Spring Boot Starter Data MongoDB
- Spring Boot Starter Validation
- Lombok
- Maven 3.9
- Java 17

## ⚠️ Consideraciones

- El build inicial puede tomar 3-5 minutos
- Requiere mínimo 2GB de RAM (t2.medium recomendado)
- MongoDB usa autenticación con usuario admin
