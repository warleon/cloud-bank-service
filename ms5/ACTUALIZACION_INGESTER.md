# 🔄 Actualización del Ingester - Modo Continuo

## 📋 CAMBIOS REALIZADOS:

### 1. **Ingester con Actualización Automática cada 1 segundo**
   - Agregado modo `continuous` que ejecuta la ingesta cada X segundos
   - Configurable mediante variables de entorno

### 2. **Queries Corregidas en Analytics**
   - Uso de `COUNT(DISTINCT)` para evitar duplicados
   - Casting explícito a `DOUBLE` para sumas numéricas
   - Validación de valores NULL

---

## 🚀 CÓMO USAR:

### **Opción 1: Despliegue con Modo Continuo (Recomendado)**

```bash
# 1. Conectar a la instancia EC2 de MS5
ssh -i tu-key.pem ubuntu@<IP-MS5>

# 2. Ir al directorio del ingester
cd ~/cloud-bank-service/ms5/datalake-ingester

# 3. Actualizar el código desde GitHub
git pull origin main

# 4. Verificar/Editar el archivo .env
nano .env

# Asegúrate de tener estas líneas:
# INGESTION_MODE=continuous
# INGESTION_INTERVAL=1

# 5. Reconstruir y levantar el servicio
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 6. Ver logs en tiempo real
docker-compose logs -f datalake-ingester

# Deberías ver:
# 🔄 Modo continuo activado - Ejecutando cada 1 segundo(s)
# 🚀 Iniciando proceso de ingesta completo
# ✅ Subidos X registros de clientes a S3...
# ⏳ Esperando 1 segundo(s) antes de la próxima ingesta...
```

### **Opción 2: Ejecutar Una Sola Vez**

```bash
# Editar .env
nano .env

# Cambiar a:
# INGESTION_MODE=once
# INGESTION_INTERVAL=1

# Ejecutar
docker-compose run --rm datalake-ingester
```

---

## ⚙️ CONFIGURACIÓN:

### **Archivo .env:**

```bash
# AWS Configuration
AWS_DEFAULT_REGION=us-east-1

# S3 Buckets
S3_BUCKET_MS1=raw-ms1-data-bgc
S3_BUCKET_MS2=raw-ms2-data-bgc
S3_BUCKET_MS4=raw-ms4-data-bgc

# PostgreSQL (MS1 - Clientes)
POSTGRES_HOST=<IP-MS1>
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=tu-password
POSTGRES_DATABASE=clientes_db

# MySQL (MS2 - Cuentas)
MYSQL_HOST=<IP-MS2>
MYSQL_PORT=3306
MYSQL_USER=admin
MYSQL_PASSWORD=tu-password
MYSQL_DATABASE=cuentas_db

# MongoDB (MS4 - Transacciones)
MONGO_HOST=<IP-MS4>
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=tu-password
MONGO_DATABASE=transacciones_db
MONGO_AUTH_SOURCE=admin

# Ingestion Configuration
INGESTION_MODE=continuous    # 'once' o 'continuous'
INGESTION_INTERVAL=1         # Segundos entre cada ingesta (1 = cada segundo)
LOG_LEVEL=INFO
```

### **Intervalos Recomendados:**

| Intervalo | Uso | Costo S3 | CPU |
|-----------|-----|----------|-----|
| **1 segundo** | Demostración en vivo | Alto | Alto |
| **5 segundos** | Desarrollo | Medio | Medio |
| **60 segundos** | Producción ligera | Bajo | Bajo |
| **3600 segundos** | Producción normal | Muy bajo | Muy bajo |

---

## 🔧 ACTUALIZAR MS5 API DE CONSULTAS:

```bash
# 1. Conectar a EC2 de MS5
ssh -i tu-key.pem ubuntu@<IP-MS5>

# 2. Ir al directorio de la API
cd ~/cloud-bank-service/ms5/api-consultas

# 3. Actualizar código desde GitHub
git pull origin main

# 4. Reconstruir y reiniciar
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 5. Verificar
docker-compose logs -f api-consultas

# 6. Probar endpoint
curl http://localhost:8000/api/dashboard | jq '.'
```

---

## ✅ VERIFICACIÓN:

### **1. Verificar que el Ingester está corriendo:**

```bash
docker-compose ps

# Debe mostrar:
# datalake-ingester ... Up
```

### **2. Ver logs en tiempo real:**

```bash
docker-compose logs -f datalake-ingester

# Deberías ver cada 1 segundo:
# 🚀 Iniciando proceso de ingesta completo
# ✅ Subidos 6 registros de clientes...
# ✅ Subidos 10 registros de cuentas...
# ⏳ Esperando 1 segundo(s)...
```

### **3. Verificar datos en S3:**

```bash
# Listar archivos en S3
aws s3 ls s3://raw-ms1-data-bgc/ --recursive
aws s3 ls s3://raw-ms2-data-bgc/ --recursive
aws s3 ls s3://raw-ms4-data-bgc/ --recursive

# Deberías ver archivos JSON recientes
```

### **4. Verificar Analytics API:**

```bash
# Dashboard ejecutivo
curl http://<IP-MS5>:8000/api/dashboard | jq '.'

# Debe mostrar:
# Total Clientes: 6 (igual que en el frontend)
# Total Cuentas: 10
# etc.
```

---

## 🛑 DETENER EL INGESTER:

```bash
# Detener servicio
docker-compose down

# O pausar sin eliminar
docker-compose stop
```

---

## ⚠️ CONSIDERACIONES IMPORTANTES:

### **1. Costo de S3:**
- Cada ingesta escribe archivos a S3
- A 1 segundo = ~86,400 escrituras/día
- **Recomendación:** Usar 60 segundos (1 minuto) en producción

### **2. Límites de Athena:**
- Athena tiene límite de queries por segundo
- Si hay muchas consultas simultáneas, puede fallar
- **Recomendación:** Usar caché en el frontend

### **3. Sincronización del Glue Crawler:**
- El Crawler debe ejecutarse periódicamente
- Recomendado: Cada 5-10 minutos
- Comando:
  ```bash
  aws glue start-crawler --name tu-crawler-name
  ```

---

## 🎯 RESULTADO ESPERADO:

1. **Frontend → Clientes:** Muestra 6 clientes ✅
2. **Analytics → Dashboard:** Muestra 6 clientes ✅
3. **Datos sincronizados cada 1 segundo** ✅
4. **Queries más precisas con DISTINCT** ✅

---

## 📊 MONITOREO:

### **Ver uso de recursos:**

```bash
# CPU y memoria del contenedor
docker stats datalake-ingester

# Logs con filtro
docker-compose logs datalake-ingester | grep "ERROR\|SUCCESS"

# Última línea de logs
docker-compose logs --tail=50 datalake-ingester
```

---

## 🐛 TROUBLESHOOTING:

### **Problema: El ingester no se actualiza**

```bash
# Forzar reconstrucción
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

### **Problema: Analytics muestra datos viejos**

```bash
# Ejecutar Glue Crawler manualmente
aws glue start-crawler --name tu-crawler-name

# Esperar 2-3 minutos y verificar
curl http://localhost:8000/api/dashboard | jq '.'
```

### **Problema: Errores de conexión a bases de datos**

```bash
# Verificar conectividad desde MS5
ping <IP-MS1>
ping <IP-MS2>
ping <IP-MS4>

# Verificar que las bases de datos estén corriendo
curl http://<IP-MS1>:8001/health
curl http://<IP-MS2>:8002/health
curl http://<IP-MS4>:8004/health
```

---

## 📝 NOTAS ADICIONALES:

- **Tiempo de propagación:** Los cambios pueden tardar 5-10 segundos en verse en Analytics (Athena cache)
- **Caché de Athena:** Athena cachea resultados por ~10 minutos
- **Sincronización:** Para datos 100% en tiempo real, considera usar Kinesis o DynamoDB Streams

---

**Última actualización:** Octubre 8, 2025  
**Autor:** Cloud Bank Team
