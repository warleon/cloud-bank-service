# 🚀 Pasos Rápidos: Configurar Analytics en Amplify

## ✅ Checklist de Implementación

### 1. Código Frontend (COMPLETADO ✓)
- [x] Actualizado `api.js` con funciones de Analytics
- [x] Actualizado `App.js` con sección Analytics
- [x] Agregado botón de navegación "📊 Analytics"
- [x] Implementados componentes visuales (dashboard, métricas, tablas)
- [x] Agregados estilos CSS para Analytics
- [x] Código pusheado a GitHub

### 2. Configurar Variable de Entorno en Amplify (PENDIENTE ⏳)

#### Acceder a Amplify Console:
1. Ve a: https://console.aws.amazon.com/amplify/
2. Selecciona tu app: `cloud-bank-app`

#### Agregar Variable de Entorno:
1. Click en **"Environment variables"** (menú izquierdo)
2. Click en **"Manage variables"**
3. Click en **"Add variable"**
4. Ingresa:
   ```
   Variable: REACT_APP_MS5_URL
   Value: http://54.196.248.70:8000
   ```
5. Click en **"Save"**

### 3. Redesplegar la Aplicación

**Opción A: Redesplegar automáticamente (Recomendado)**
- Amplify detectará el push a GitHub y desplegará automáticamente
- Ve a la pestaña **"Deployments"** para ver el progreso
- Espera 3-5 minutos

**Opción B: Redesplegar manualmente**
1. Ve a la pestaña **"Deployments"**
2. Click en **"Redeploy this version"**
3. Espera a que complete

### 4. Verificar Configuración (DESPUÉS DEL DEPLOY)

#### A. Verificar Build
1. En Amplify Console → **"Deployments"**
2. Asegúrate que el build sea exitoso (verde)
3. Click en el deployment para ver logs

#### B. Probar la Aplicación
1. Abre tu app: `https://[tu-app-id].amplifyapp.com`
2. Click en el botón **"📊 Analytics"**
3. Espera 5-10 segundos (Athena queries son lentas)
4. Deberías ver:
   - ✅ Dashboard con 6 métricas principales
   - ✅ Análisis de cuentas por tipo
   - ✅ Análisis de transacciones
   - ✅ Clientes VIP

#### C. Verificar en Browser Console (F12)
1. Abre DevTools → Pestaña **Network**
2. Filtra por: `54.196.248.70`
3. Deberías ver requests a:
   - `http://54.196.248.70:8000/api/dashboard`
   - `http://54.196.248.70:8000/api/cuentas/resumen`
   - `http://54.196.248.70:8000/api/transacciones/resumen`
   - `http://54.196.248.70:8000/api/analisis/clientes-vip`
4. Todos deben retornar **Status 200 OK**

## 🔧 Troubleshooting

### Error: Network Error / CORS
**Problema:** El navegador bloquea la request por CORS

**Solución:** Verifica CORS en `ms5/api-consultas/main.py`:
```bash
# Conéctate a EC2 MS5
ssh -i tu-key.pem ubuntu@54.196.248.70

# Verifica el archivo main.py
cd ~/ms5/api-consultas
grep -A 10 "CORSMiddleware" main.py

# Si no tiene CORS, edita main.py y agrega:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Reinicia el contenedor
docker-compose restart
```

### Error: Timeout / Query tarda mucho
**Problema:** Athena queries pueden ser lentas la primera vez

**Solución:**
- Primera query puede tomar 10-15 segundos (Athena warming up)
- Queries subsecuentes son más rápidas (cache)
- Si persiste, verifica logs:
  ```bash
  docker logs api-consultas-1
  ```

### No se ven datos / Empty response
**Problema:** No hay datos en el DataLake

**Verificación:**
```bash
# Verifica que el ingester haya corrido
cd ~/ms5/datalake-ingester
docker-compose logs

# Verifica S3 buckets
aws s3 ls s3://raw-ms1-data-bgc/
aws s3 ls s3://raw-ms2-data-bgc/
aws s3 ls s3://raw-ms4-data-bgc/

# Verifica Glue Catalog
aws glue get-tables --database-name cloud_bank_db
```

### Security Group bloqueando puerto 8000
**Problema:** EC2 no acepta conexiones en puerto 8000

**Solución:**
1. Ve a EC2 Console → Security Groups
2. Encuentra el SG de MS5
3. Agrega regla Inbound:
   - Type: Custom TCP
   - Port: 8000
   - Source: 0.0.0.0/0 (o solo la IP de Amplify)

## 📊 Endpoints Disponibles

Una vez funcionando, Analytics mostrará:

### Dashboard Ejecutivo
- Total de clientes
- Total de cuentas
- Total de transacciones
- Volumen total transaccionado
- Saldo promedio por cuenta
- Transacción promedio

### Análisis de Cuentas
- Distribución por tipo de cuenta
- Saldos totales y promedios
- Cantidad de cuentas por tipo

### Análisis de Transacciones
- Distribución por tipo de transacción
- Montos totales y promedios
- Volumen transaccional

### Clientes VIP
- Top 10 clientes con mayor patrimonio
- Total de cuentas por cliente
- Patrimonio total y promedio

## 🎯 Resultado Esperado

Después de completar estos pasos, tu aplicación tendrá:

✅ **Frontend completo con 4 secciones:**
- 👤 Clientes (MS1)
- 💳 Cuentas (MS2)
- 💸 Transacciones (MS4)
- 📊 Analytics (MS5) ← **NUEVO**

✅ **DataLake Analytics funcionando:**
- Datos en S3 (3 buckets)
- Catálogo en Glue (5 tablas)
- Queries en Athena
- API REST en FastAPI
- Visualización en React

✅ **Arquitectura completa de microservicios:**
```
Frontend (Amplify)
    ↓
API Gateway (opcional)
    ↓
EC2 Instances
    ├── MS1 (PostgreSQL) → Clientes
    ├── MS2 (MySQL) → Cuentas
    ├── MS4 (MongoDB) → Transacciones
    └── MS5 (Athena/S3) → Analytics
```

## 📝 Notas Finales

- **IP Actual MS5:** `54.196.248.70:8000`
- **Health Check:** http://54.196.248.70:8000/health
- **API Docs:** http://54.196.248.70:8000/docs
- **Database:** `cloud_bank_db`
- **S3 Output:** `s3://athena-results-cloud-bank-bgc/`

⚠️ **Importante:** Si tu sesión de AWS Academy se reinicia, la IP cambiará y deberás actualizar `REACT_APP_MS5_URL` en Amplify.
