# 🏦 Cloud Bank Service - Arquitectura de Microservicios

Sistema bancario completo construido con arquitectura de microservicios en AWS.

## 📋 Tabla de Contenidos

- [Arquitectura General](#arquitectura-general)
- [Microservicios](#microservicios)
- [Tecnologías](#tecnologías)
- [Guía de Despliegue](#guía-de-despliegue)
- [Estructura del Proyecto](#estructura-del-proyecto)

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Amplify (Frontend)                    │
│                    React + Axios                             │
└─────────────────┬───────────────┬───────────────┬───────────┘
                  │               │               │
         ┌────────▼─────┐  ┌─────▼──────┐  ┌────▼─────────┐
         │   MS1 (EC2)  │  │ MS2 (EC2)  │  │  MS4 (EC2)   │
         │   Clientes   │  │  Cuentas   │  │Transacciones │
         │   Python     │  │  Node.js   │  │    Java      │
         │   FastAPI    │  │  Express   │  │ Spring Boot  │
         │   :8001      │  │   :8002    │  │    :8004     │
         └──────┬───────┘  └─────┬──────┘  └──────┬───────┘
                │                │                 │
         ┌──────▼───────┐ ┌─────▼──────┐  ┌──────▼───────┐
         │  PostgreSQL  │ │   MySQL    │  │   MongoDB    │
         │    :5432     │ │   :3306    │  │   :27017     │
         └──────────────┘ └────────────┘  └──────────────┘
                                │
                         ┌──────▼──────┐
                         │  MS5 (EC2)  │
                         │  DataLake   │
                         │   Athena    │
                         └─────────────┘
```

## 🎯 Microservicios

### MS1 - Gestión de Clientes
- **Lenguaje**: Python 3.11
- **Framework**: FastAPI
- **Base de Datos**: PostgreSQL 15
- **Puerto**: 8001
- **Función**: Registro y gestión de clientes bancarios con documentos de identidad
- **Tablas**: `clientes`, `documentos_identidad`

### MS2 - Gestión de Cuentas
- **Lenguaje**: Node.js 18
- **Framework**: Express
- **Base de Datos**: MySQL 8.0
- **Puerto**: 8002
- **Función**: Creación y administración de cuentas bancarias (Sueldo, Free, Premium, Ahorro)
- **Tablas**: `tipos_cuenta`, `cuentas`

### MS4 - Gestión de Transacciones
- **Lenguaje**: Java 17
- **Framework**: Spring Boot 3.2.1
- **Base de Datos**: MongoDB 7.0
- **Puerto**: 8004
- **Función**: Registro y seguimiento de transacciones (Depósitos, Retiros, Transferencias, Pagos)
- **Colecciones**: `transacciones`

### MS5 - DataLake & Analytics
- **Ubicación**: `m5/`
- **Función**: Ingesta de datos a S3, catalogación con Glue, consultas con Athena
- **Ver**: [m5/README.md](m5/README.md)

### Frontend
- **Framework**: React 18
- **Despliegue**: AWS Amplify
- **Función**: Interfaz de usuario para cajeros bancarios
- **Conexión**: REST APIs con MS1, MS2, MS4

## 🛠️ Tecnologías

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| MS1 API | Python + FastAPI | 3.11 / 0.104.1 |
| MS1 DB | PostgreSQL | 15 |
| MS2 API | Node.js + Express | 18 / 4.18.2 |
| MS2 DB | MySQL | 8.0 |
| MS4 API | Java + Spring Boot | 17 / 3.2.1 |
| MS4 DB | MongoDB | 7.0 |
| Frontend | React | 18.2.0 |
| Contenedores | Docker + Docker Compose | Latest |
| Cloud | AWS (EC2, S3, Glue, Athena, Amplify) | - |

## 🚀 Guía de Despliegue

### ⚡ Despliegue Automático con Reintentos

**¡NUEVO!** Todos los microservicios ahora incluyen **reintentos automáticos** para conectarse a sus bases de datos. Esto garantiza que el despliegue sea completamente automático sin intervención manual.

📖 **Documentación completa**: [AUTO_DEPLOY.md](./AUTO_DEPLOY.md)

#### Despliegue con Script Maestro

```bash
# Clonar repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service

# Ejecutar despliegue automático de TODOS los microservicios
chmod +x deploy-all.sh
./deploy-all.sh
```

El script desplegará automáticamente MS1, MS2 y MS4 con reintentos inteligentes.

#### Características del Sistema de Reintentos

- ✅ **MS1 (Python)**: 5 reintentos con 5s de espera (máx 25s)
- ✅ **MS2 (Node.js)**: 5 reintentos con 5s de espera (máx 25s)
- ✅ **MS4 (Java)**: Timeouts de 30s con reintentos automáticos
- ✅ **Docker Compose**: `restart: on-failure` en todos los servicios
- ✅ **Logs claros**: Indica cada intento de conexión

### Prerrequisitos
- Cuenta de AWS Academy (Vocareum) o AWS regular
- 3 instancias EC2 Ubuntu 22.04 (t2.medium o t2.large)
- Docker y Docker Compose instalados
- Git instalado

### Paso 1: Configurar Instancias EC2

Para **cada microservicio** (MS1, MS2, MS4):

```bash
# 1. Lanzar instancia EC2
# - AMI: Ubuntu Server 22.04 LTS
# - Tipo: 
#   * MS1, MS2: t2.small (mínimo)
#   * MS4: t2.medium (Java requiere más recursos)
# - Storage: 20GB
# - Security Group: Permitir SSH (22) + Puerto del MS

# 2. Configurar Security Groups
# MS1: Permitir 22, 8001, 5432
# MS2: Permitir 22, 8002, 3306
# MS4: Permitir 22, 8004, 27017

# 3. Conectar a EC2
ssh -i tu-key.pem ubuntu@<EC2-IP>

# 4. Instalar Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# 5. Cerrar sesión y reconectar para aplicar permisos
exit
ssh -i tu-key.pem ubuntu@<EC2-IP>
```

### Paso 2: Desplegar Microservicios

**En cada instancia EC2**:

```bash
# 1. Clonar repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service

# 2. Navegar al microservicio correspondiente
cd ms1  # o ms2, ms4 según la instancia

# 3. Levantar servicios
docker-compose up -d

# 4. Ver logs
docker-compose logs -f

# 5. Verificar estado
docker-compose ps
```

### Paso 3: Verificar Conectividad

Prueba cada API desde tu navegador o con `curl`:

```bash
# MS1 - Clientes
curl http://<EC2-MS1-IP>:8001/
curl http://<EC2-MS1-IP>:8001/clientes

# MS2 - Cuentas
curl http://<EC2-MS2-IP>:8002/
curl http://<EC2-MS2-IP>:8002/cuentas

# MS4 - Transacciones
curl http://<EC2-MS4-IP>:8004/
curl http://<EC2-MS4-IP>:8004/transacciones
```

### Paso 4: Desplegar Frontend en AWS Amplify

```bash
# 1. Push código a GitHub
git add .
git commit -m "Complete banking system"
git push origin main

# 2. Configurar AWS Amplify
# - Ir a AWS Amplify Console
# - New app → Host web app → GitHub
# - Seleccionar repositorio: cloud-bank-service
# - Base directory: frontend
# - Build command: npm run build
# - Build output directory: build

# 3. Agregar variables de entorno en Amplify:
REACT_APP_MS1_URL=http://<EC2-MS1-IP>:8001
REACT_APP_MS2_URL=http://<EC2-MS2-IP>:8002
REACT_APP_MS4_URL=http://<EC2-MS4-IP>:8004

# 4. Save and deploy
```

### Paso 5: Probar Sistema Completo

1. Abrir URL de Amplify en navegador
2. Ir a módulo "Clientes" → Registrar un cliente
3. Ir a módulo "Cuentas" → Crear cuenta para el cliente
4. Ir a módulo "Transacciones" → Realizar depósito a la cuenta
5. Verificar transacciones en el historial

## 📁 Estructura del Proyecto

```
cloud-bank-service/
│
├── ms1/                          # Microservicio 1 - Clientes
│   ├── api/
│   │   ├── main.py              # FastAPI app
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   ├── init-db.sql              # Schema PostgreSQL
│   └── README.md
│
├── ms2/                          # Microservicio 2 - Cuentas
│   ├── api/
│   │   ├── server.js            # Express app
│   │   ├── package.json
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   ├── init-db.sql              # Schema MySQL
│   └── README.md
│
├── ms4/                          # Microservicio 4 - Transacciones
│   ├── api/
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── java/com/cloudbank/transacciones/
│   │   │       │   ├── TransaccionesApplication.java
│   │   │       │   ├── model/Transaccion.java
│   │   │       │   ├── repository/TransaccionRepository.java
│   │   │       │   ├── service/TransaccionService.java
│   │   │       │   └── controller/TransaccionController.java
│   │   │       └── resources/
│   │   │           └── application.properties
│   │   ├── pom.xml
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   ├── init-mongo.js            # Schema MongoDB
│   └── README.md
│
├── m5/                           # Microservicio 5 - DataLake
│   ├── api-consultas/           # API Athena
│   ├── datalake-ingester/       # Ingestores ETL
│   ├── ms-databases/            # DBs de prueba
│   ├── docker-compose.yml
│   └── README.md
│
├── frontend/                     # Frontend React
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── api.js               # Axios clients
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── README.md
│
├── README.md                     # Este archivo
├── DEPLOYMENT_GUIDE.md          # Guía detallada paso a paso
├── .gitignore
└── amplify.yml                  # Config de Amplify
```

## 🔗 Flujo de Datos

```
1. Usuario registra cliente en Frontend
   → POST a MS1 /clientes
   → Guarda en PostgreSQL

2. Usuario crea cuenta para cliente
   → POST a MS2 /cuentas con cliente_id
   → Guarda en MySQL

3. Usuario realiza transacción
   → POST a MS4 /transacciones con cuenta_id
   → Guarda en MongoDB

4. DataLake (MS5) ingesta datos periódicamente
   → Extrae de PostgreSQL, MySQL, MongoDB
   → Carga a S3 en formato JSON Lines
   → Glue cataloga datos
   → Athena permite consultas analíticas
```

## 📊 APIs REST

### MS1 - Clientes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clientes` | Listar clientes |
| POST | `/clientes` | Crear cliente |
| GET | `/clientes/{id}` | Obtener cliente |
| PUT | `/clientes/{id}` | Actualizar cliente |
| DELETE | `/clientes/{id}` | Eliminar cliente |

### MS2 - Cuentas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tipos-cuenta` | Listar tipos de cuenta |
| GET | `/cuentas` | Listar cuentas |
| POST | `/cuentas` | Crear cuenta |
| GET | `/cuentas/{id}` | Obtener cuenta |
| GET | `/cuentas/cliente/{id}` | Cuentas por cliente |
| PATCH | `/cuentas/{id}/saldo` | Actualizar saldo |

### MS4 - Transacciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/transacciones` | Listar transacciones |
| POST | `/transacciones` | Crear transacción |
| GET | `/transacciones/{id}` | Obtener transacción |
| GET | `/transacciones/cuenta/{id}` | Transacciones por cuenta |
| PATCH | `/transacciones/{id}/estado` | Actualizar estado |

Ver READMEs individuales para detalles completos de cada API.

## 🐳 Docker Hub (Opcional)

Si deseas publicar las imágenes en Docker Hub:

```bash
# Login
docker login -u tu-usuario

# Build y Push MS1
cd ms1/api
docker build -t tu-usuario/cloud-bank-ms1:api-clientes .
docker push tu-usuario/cloud-bank-ms1:api-clientes

# Build y Push MS2
cd ../../ms2/api
docker build -t tu-usuario/cloud-bank-ms2:api-cuentas .
docker push tu-usuario/cloud-bank-ms2:api-cuentas

# Build y Push MS4
cd ../../ms4/api
docker build -t tu-usuario/cloud-bank-ms4:api-transacciones .
docker push tu-usuario/cloud-bank-ms4:api-transacciones
```

Luego actualiza los `image:` en los docker-compose.yml.

## 🔒 Seguridad

### Security Groups
- **MS1 EC2**: Permitir 22 (SSH), 8001 (API), 5432 (PostgreSQL)
- **MS2 EC2**: Permitir 22 (SSH), 8002 (API), 3306 (MySQL)
- **MS4 EC2**: Permitir 22 (SSH), 8004 (API), 27017 (MongoDB)

### CORS
Todas las APIs tienen CORS habilitado para permitir peticiones del frontend en Amplify.

### Credenciales
Las credenciales por defecto son para desarrollo. En producción:
- Usar AWS Secrets Manager
- Variables de entorno seguras
- Roles IAM apropiados

## 📈 Escalabilidad

Para escalar horizontalmente:

1. **Auto Scaling Groups**: Configura ASG para cada tipo de microservicio
2. **Load Balancers**: Agrega ALB delante de cada grupo de instancias
3. **Bases de datos**: Usa servicios administrados (RDS, DocumentDB)
4. **Caché**: Implementa Redis/ElastiCache
5. **CDN**: CloudFront para el frontend

## 🔄 CI/CD

Sugerencias para implementar CI/CD:

```yaml
# GitHub Actions ejemplo (.github/workflows/deploy.yml)
name: Deploy Microservices
on:
  push:
    branches: [main]
jobs:
  deploy-ms1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to EC2
        run: |
          ssh -i ${{ secrets.EC2_KEY }} ubuntu@${{ secrets.EC2_MS1_IP }} \
          "cd cloud-bank-service/ms1 && git pull && docker-compose up -d --build"
```

## 📝 Monitoreo

Herramientas recomendadas:
- **CloudWatch**: Métricas y logs de EC2
- **Application Performance Monitoring**: New Relic, Datadog
- **Prometheus + Grafana**: Métricas personalizadas
- **ELK Stack**: Logging centralizado

## 🧪 Testing

Cada microservicio incluye datos de ejemplo para testing:
- **MS1**: 3 clientes de ejemplo
- **MS2**: 4 tipos de cuenta, 4 cuentas de ejemplo
- **MS4**: 5 transacciones de ejemplo

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es para fines educativos.

## 👥 Autores

- Cloud Bank Team

## 🆘 Soporte

Si tienes problemas:

1. Revisa **DEPLOYMENT_GUIDE.md** para guía detallada paso a paso
2. Consulta los logs: `docker-compose logs -f`
3. Verifica conectividad: `curl http://localhost:PORT/health`
4. Confirma Security Groups en AWS
5. Verifica variables de entorno

---

**¡Buen despliegue! 🚀**