# 🔄 ACTUALIZACIÓN DE IPs PÚBLICAS - Cloud Bank Service

**Fecha:** Octubre 8, 2025  
**Motivo:** Las IPs públicas de AWS EC2 cambiaron después de reiniciar las instancias

---

## 📋 NUEVAS IPs PÚBLICAS:

| Microservicio | IP Pública Nueva | Puerto API | Puerto BD |
|---------------|------------------|------------|-----------|
| **MS1** (Clientes) | `34.201.99.218` | 8001 | 5432 (PostgreSQL) |
| **MS2** (Cuentas) | `13.222.184.86` | 8002 | 3306 (MySQL) |
| **MS3** (Agregador) | `98.88.19.214` | 6000 | N/A |
| **MS4** (Transacciones) | `3.90.218.198` | 8004 | 27017 (MongoDB) |
| **MS5** (Analytics) | `3.95.211.15` | 8000 | N/A |

---

## 🚀 PASOS DE ACTUALIZACIÓN:

### **PASO 1: Actualizar MS3 (Agregador)**

MS3 consume datos de MS1, MS2 y MS4. Necesita saber las nuevas IPs.

```bash
# Conectar a MS3
ssh -i tu-key.pem ubuntu@98.88.19.214

# Ir al directorio
cd ~/cloud-bank-service/ms3

# Crear/Editar archivo .env
nano .env
```

**Agregar estas líneas:**
```bash
MS1_URL=http://34.201.99.218:8001
MS2_URL=http://13.222.184.86:8002
MS4_URL=http://3.90.218.198:8004
LOG_LEVEL=INFO
```

**Guardar y reiniciar:**
```bash
docker-compose down
docker-compose up -d

# Verificar
docker-compose logs -f
```

---

### **PASO 2: Actualizar MS5 Datalake Ingester**

El ingester necesita conectar a las bases de datos de MS1, MS2, MS4.

```bash
# Conectar a MS5
ssh -i tu-key.pem ubuntu@3.95.211.15

# Ir al directorio del ingester
cd ~/cloud-bank-service/ms5/datalake-ingester

# Editar .env
nano .env
```

**Actualizar estas líneas:**
```bash
# PostgreSQL Database (MS1 - Clientes)
POSTGRES_HOST=34.201.99.218
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DATABASE=clientes_db

# MySQL Database (MS2 - Cuentas)
MYSQL_HOST=13.222.184.86
MYSQL_PORT=3306
MYSQL_USER=admin
MYSQL_PASSWORD=admin123
MYSQL_DATABASE=cuentas_db

# MongoDB Database (MS4 - Transacciones)
MONGO_HOST=3.90.218.198
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=admin123
MONGO_DATABASE=transacciones_db
MONGO_AUTH_SOURCE=admin

# Ingestion Mode
INGESTION_MODE=once
INGESTION_INTERVAL=60
```

**⚠️ IMPORTANTE:** Antes de reiniciar, necesitas configurar Security Groups (ver PASO 3)

---

### **PASO 3: Configurar Security Groups en AWS**

Desde AWS Console o CLI, agrega estas reglas:

#### **Security Group de MS1:**
```
Inbound Rules:
├── Type: SSH, Port: 22, Source: Tu IP
├── Type: HTTP (Custom TCP), Port: 8001, Source: 0.0.0.0/0
└── Type: PostgreSQL, Port: 5432, Source: 3.95.211.15/32 (IP de MS5)
```

#### **Security Group de MS2:**
```
Inbound Rules:
├── Type: SSH, Port: 22, Source: Tu IP
├── Type: HTTP (Custom TCP), Port: 8002, Source: 0.0.0.0/0
└── Type: MySQL/Aurora, Port: 3306, Source: 3.95.211.15/32 (IP de MS5)
```

#### **Security Group de MS4:**
```
Inbound Rules:
├── Type: SSH, Port: 22, Source: Tu IP
├── Type: HTTP (Custom TCP), Port: 8004, Source: 0.0.0.0/0
└── Type: Custom TCP, Port: 27017, Source: 3.95.211.15/32 (IP de MS5)
```

**Comando AWS CLI (alternativa rápida para desarrollo):**
```bash
# Obtener IDs de Security Groups
MS1_SG=$(aws ec2 describe-instances \
  --filters "Name=ip-address,Values=34.201.99.218" \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
  --output text)

MS2_SG=$(aws ec2 describe-instances \
  --filters "Name=ip-address,Values=13.222.184.86" \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
  --output text)

MS4_SG=$(aws ec2 describe-instances \
  --filters "Name=ip-address,Values=3.90.218.198" \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
  --output text)

# Agregar reglas (permitir desde MS5)
aws ec2 authorize-security-group-ingress \
  --group-id $MS1_SG --protocol tcp --port 5432 \
  --cidr 3.95.211.15/32

aws ec2 authorize-security-group-ingress \
  --group-id $MS2_SG --protocol tcp --port 3306 \
  --cidr 3.95.211.15/32

aws ec2 authorize-security-group-ingress \
  --group-id $MS4_SG --protocol tcp --port 27017 \
  --cidr 3.95.211.15/32
```

---

### **PASO 4: Actualizar Frontend (React)**

El frontend necesita las nuevas IPs de las APIs.

```bash
# Si usas AWS Amplify, actualiza las variables de entorno:
REACT_APP_MS1_URL=http://34.201.99.218:8001
REACT_APP_MS2_URL=http://13.222.184.86:8002
REACT_APP_MS3_URL=http://98.88.19.214:6000
REACT_APP_MS4_URL=http://3.90.218.198:8004
REACT_APP_MS5_URL=http://3.95.211.15:8000

# Redeploy en Amplify para aplicar cambios
```

Si tienes el frontend local:
```bash
cd frontend
nano .env

# Actualizar URLs
npm run build
```

---

## ✅ VALIDACIÓN DESPUÉS DE ACTUALIZAR:

### **1. Verificar APIs están respondiendo:**
```bash
curl http://34.201.99.218:8001/health
curl http://13.222.184.86:8002/health
curl http://98.88.19.214:6000/health
curl http://3.90.218.198:8004/health
curl http://3.95.211.15:8000/health
```

### **2. Probar conectividad de MS5 a las bases de datos:**
```bash
# Desde MS5
ssh -i tu-key.pem ubuntu@3.95.211.15

# Instalar herramientas de red
sudo apt install -y netcat-openbsd telnet

# Probar conexiones
nc -zv 34.201.99.218 5432  # PostgreSQL
nc -zv 13.222.184.86 3306  # MySQL
nc -zv 3.90.218.198 27017  # MongoDB

# Si todos dicen "succeeded", está OK ✅
```

### **3. Ejecutar el ingester:**
```bash
cd ~/cloud-bank-service/ms5/datalake-ingester

# Ejecutar una vez
docker-compose run --rm datalake-ingester python run_ingestion.py

# Deberías ver:
# ✅ Subidos 6 registros de clientes...
# ✅ Subidos 10 registros de cuentas...
# ✅ Subidos 12 transacciones...
```

### **4. Verificar Analytics:**
```bash
curl http://3.95.211.15:8000/api/dashboard | jq '.data[] | select(.metrica=="Total Clientes")'

# Debe mostrar: "valor": "6"
```

### **5. Verificar MS3 (Agregador):**
```bash
# Obtener perfil completo de un cliente
curl http://98.88.19.214:6000/api/clientes/1/perfil-completo | jq '.'

# Debe mostrar datos de MS1, MS2 y MS4 combinados
```

---

## 🔄 SCRIPTS DE VALIDACIÓN:

### **Script 1: Validar todas las APIs**
```bash
#!/bin/bash
echo "🔍 Validando APIs..."
for url in \
  "http://34.201.99.218:8001/health" \
  "http://13.222.184.86:8002/health" \
  "http://98.88.19.214:6000/health" \
  "http://3.90.218.198:8004/health" \
  "http://3.95.211.15:8000/health"
do
  status=$(curl -s -o /dev/null -w "%{http_code}" $url)
  if [ $status -eq 200 ]; then
    echo "✅ $url - OK"
  else
    echo "❌ $url - FAIL (HTTP $status)"
  fi
done
```

### **Script 2: Validar conectividad de bases de datos desde MS5**
```bash
#!/bin/bash
echo "🔍 Validando conectividad a bases de datos..."
nc -zv -w 3 34.201.99.218 5432 2>&1 | grep -q succeeded && echo "✅ PostgreSQL (MS1)" || echo "❌ PostgreSQL (MS1)"
nc -zv -w 3 13.222.184.86 3306 2>&1 | grep -q succeeded && echo "✅ MySQL (MS2)" || echo "❌ MySQL (MS2)"
nc -zv -w 3 3.90.218.198 27017 2>&1 | grep -q succeeded && echo "✅ MongoDB (MS4)" || echo "❌ MongoDB (MS4)"
```

---

## 📊 RESUMEN DE CAMBIOS:

| Archivo | Cambios |
|---------|---------|
| `ms3/.env` | Actualizar URLs de MS1, MS2, MS4 |
| `ms5/datalake-ingester/.env` | Actualizar IPs de PostgreSQL, MySQL, MongoDB |
| Frontend env | Actualizar URLs de todas las APIs |
| AWS Security Groups | Permitir MS5 → MS1:5432, MS2:3306, MS4:27017 |

---

## ⚠️ NOTAS IMPORTANTES:

1. **IPs Públicas vs Privadas:**
   - Estamos usando IPs públicas
   - Si las instancias están en la misma VPC, considera usar IPs privadas para ahorrar costos y mejorar seguridad

2. **IPs Elásticas:**
   - Las IPs públicas cambian cada vez que reinicias la instancia
   - Considera usar **Elastic IPs** (IPs estáticas) para evitar este problema

3. **Security Groups:**
   - Actualmente permitiendo desde IP específica de MS5 (más seguro)
   - En desarrollo puedes usar 0.0.0.0/0 pero es menos seguro

4. **Modo Ingester:**
   - Por ahora dejé `INGESTION_MODE=once`
   - Después de validar, puedes cambiar a `continuous` con intervalo de 60 segundos

---

## 🎯 ORDEN DE EJECUCIÓN RECOMENDADO:

1. ✅ Actualizar Security Groups (PASO 3)
2. ✅ Actualizar MS3 .env (PASO 1)
3. ✅ Actualizar MS5 ingester .env (PASO 2)
4. ✅ Probar conectividad (Validación 2)
5. ✅ Ejecutar ingester (Validación 3)
6. ✅ Verificar Analytics (Validación 4)
7. ✅ Actualizar Frontend (PASO 4)

---

**¿Necesitas ayuda con algún paso específico?** 🚀
