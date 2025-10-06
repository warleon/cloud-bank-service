# 🚀 Configuración de API Gateway para MS5 DataLake Analytics

## 📋 Resumen

Este API Gateway actúa como proxy entre el frontend (Amplify) y el backend (EC2 MS5), proporcionando:
- ✅ **HTTPS** en lugar de HTTP
- ✅ **URL pública estable** que no cambia con los reinicios de EC2
- ✅ **CORS** configurado correctamente
- ✅ **Seguridad mejorada** (no expones directamente el puerto 8000)

## 🏗️ Arquitectura

```
Frontend (Amplify)
    ↓ HTTPS
API Gateway (AWS)
    ↓ HTTP
EC2 MS5 (54.196.248.70:8000)
    ↓
FastAPI (api-consultas)
    ↓
Amazon Athena → S3 DataLake
```

## 🔧 Configuración Paso a Paso

### 1. Crear HTTP API en API Gateway

1. Ve a: https://console.aws.amazon.com/apigateway/
2. Click en **"Create API"**
3. Selecciona **"HTTP API"** → Click en **"Build"**

### 2. Configurar Integration

**Add integration:**
- Type: **HTTP**
- URL endpoint: `http://54.196.248.70:8000`
- Name: `ms5-datalake-analytics`
- Method: **ANY**

**API name:**
- Name: `cloud-bank-ms5-api`

Click **"Next"**

### 3. Configurar Routes

**Route:**
- Method: **ANY**
- Resource path: `/{proxy+}`
- Integration: `ms5-datalake-analytics`

Click **"Next"**

### 4. Configurar Stage

**Stage name:** `prod` o `$default`
**Auto-deploy:** ✅ Enabled

Click **"Next"** → **"Create"**

### 5. Configurar CORS

1. En tu API, ve a **"CORS"** (menú lateral)
2. Click en **"Configure"**
3. Configura:
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
   Access-Control-Allow-Methods: GET,POST,OPTIONS,PUT,DELETE
   Access-Control-Max-Age: 86400
   ```
4. Click **"Save"**

### 6. Obtener Invoke URL

1. Ve a **"Stages"** (menú lateral)
2. Copia la **"Invoke URL"**
   - Ejemplo: `https://abc123xyz.execute-api.us-east-1.amazonaws.com`

## 🧪 Testing del API Gateway

### Verificar Health Check

```powershell
# PowerShell
curl https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com/health
```

```bash
# Linux/Mac
curl https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "athena_connection": "ok",
  "timestamp": "2025-10-06T04:00:00.000000"
}
```

### Probar Endpoints de Analytics

```powershell
# Dashboard ejecutivo
curl https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com/api/dashboard

# Resumen de cuentas
curl https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com/api/cuentas/resumen

# Resumen de transacciones
curl https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com/api/transacciones/resumen

# Clientes VIP
curl https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com/api/analisis/clientes-vip?patrimonio_minimo=10000&limit=10
```

## 🔐 Configuración de Seguridad (Opcional)

### Restringir Origins en CORS (Producción)

En lugar de `*`, especifica tu dominio de Amplify:

```
Access-Control-Allow-Origin: https://main.d1234567890.amplifyapp.com
```

### Agregar API Key (Opcional)

1. En API Gateway, ve a **"API Keys"**
2. Crea una nueva API Key
3. Crea un **Usage Plan** y asocia tu API
4. En el frontend, agrega el header:
   ```javascript
   headers: {
     'x-api-key': 'tu-api-key'
   }
   ```

### Configurar Throttling (Opcional)

1. En **"Stages"** → **"Throttling"**
2. Configura:
   - Rate limit: 1000 requests/segundo
   - Burst limit: 2000 requests

## 🌐 Configuración en AWS Amplify

### Variable de Entorno

1. Ve a: https://console.aws.amazon.com/amplify/
2. Selecciona tu app: `cloud-bank-app`
3. Click en **"Environment variables"**
4. Agrega:
   ```
   Variable: REACT_APP_MS5_URL
   Value: https://TU-API-GATEWAY-URL.execute-api.us-east-1.amazonaws.com
   ```
5. **Nota:** NO incluyas `/prod` o `/` al final

### Redesplegar

1. Ve a **"Deployments"**
2. Click en `⋮` → **"Redeploy this version"**
3. Espera 3-5 minutos

## 📊 Endpoints Disponibles

Todos estos endpoints ahora están disponibles a través de API Gateway:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/dashboard` | GET | Dashboard ejecutivo |
| `/api/clientes/resumen` | GET | Resumen de clientes |
| `/api/clientes/lista` | GET | Lista de clientes |
| `/api/clientes/con-cuentas` | GET | Clientes con cuentas |
| `/api/cuentas/resumen` | GET | Resumen de cuentas |
| `/api/cuentas/por-tipo` | GET | Cuentas por tipo |
| `/api/cuentas/top-saldos` | GET | Top cuentas por saldo |
| `/api/transacciones/resumen` | GET | Resumen de transacciones |
| `/api/transacciones/por-tipo` | GET | Transacciones por tipo |
| `/api/transacciones/por-estado` | GET | Transacciones por estado |
| `/api/transacciones/recientes` | GET | Transacciones recientes |
| `/api/transacciones/detalladas` | GET | Transacciones detalladas |
| `/api/analisis/clientes-vip` | GET | Clientes VIP |
| `/api/analisis/actividad-diaria` | GET | Actividad últimos 30 días |

## 🔍 Troubleshooting

### Error: 502 Bad Gateway

**Causa:** API Gateway no puede conectarse al EC2

**Soluciones:**
1. Verifica que EC2 MS5 esté corriendo
2. Verifica que docker-compose esté activo:
   ```bash
   ssh -i tu-key.pem ubuntu@54.196.248.70
   cd ~/ms5/api-consultas
   docker-compose ps
   ```
3. Reinicia el servicio:
   ```bash
   docker-compose restart
   ```

### Error: CORS Policy

**Causa:** CORS no configurado correctamente

**Solución:**
1. Ve a API Gateway → CORS
2. Verifica que `allow_origins` incluya `*` o tu dominio de Amplify
3. Verifica que `main.py` en MS5 tenga CORS habilitado (ya está configurado)

### Error: Timeout

**Causa:** Query de Athena tarda mucho

**Solución:**
- Primera query puede tomar 10-15 segundos
- Queries subsecuentes son más rápidas (cache de Athena)
- Verifica logs en EC2:
  ```bash
  docker logs api-consultas-1 -f
  ```

### Error: IP de EC2 cambió

**Causa:** Reinicio de AWS Academy cambia la IP pública

**Solución:**
1. Obtén la nueva IP de EC2
2. Ve a API Gateway → Integrations
3. Edita la integration `ms5-datalake-analytics`
4. Actualiza la URL: `http://NUEVA-IP:8000`
5. Deploy automático se aplicará

## 📝 Ventajas del API Gateway

| Aspecto | Sin API Gateway | Con API Gateway |
|---------|----------------|-----------------|
| **Protocolo** | HTTP | HTTPS ✅ |
| **URL** | http://54.196.248.70:8000 | https://abc.execute-api... |
| **IP cambia** | Sí, cada restart | No, URL estable ✅ |
| **CORS** | Configurar en FastAPI | Configurado en AWS ✅ |
| **Seguridad** | Puerto expuesto | Proxy seguro ✅ |
| **Throttling** | No | Configurable ✅ |
| **Logs** | Solo en EC2 | CloudWatch Logs ✅ |
| **Monitoreo** | Manual | CloudWatch Metrics ✅ |

## 📊 Monitoreo con CloudWatch

### Ver Métricas

1. Ve a API Gateway → tu API → **"Monitor"**
2. Verás:
   - Count (requests)
   - Latency (tiempo de respuesta)
   - 4xx Errors
   - 5xx Errors

### Ver Logs

1. Ve a CloudWatch → **"Logs"**
2. Busca el log group: `/aws/apigateway/cloud-bank-ms5-api`
3. Verás todas las requests con detalles

## 🎯 Configuración Completa

Una vez configurado:

```javascript
// frontend/src/api.js (YA ESTÁ CONFIGURADO)
const API_ENDPOINTS = {
  clientes: process.env.REACT_APP_MS1_URL,
  cuentas: process.env.REACT_APP_MS2_URL,
  transacciones: process.env.REACT_APP_MS4_URL,
  analytics: process.env.REACT_APP_MS5_URL  // API Gateway URL
};
```

```bash
# AWS Amplify Environment Variables
REACT_APP_MS1_URL=https://api-gateway-ms1...
REACT_APP_MS2_URL=https://api-gateway-ms2...
REACT_APP_MS4_URL=https://api-gateway-ms4...
REACT_APP_MS5_URL=https://abc123.execute-api.us-east-1.amazonaws.com
```

## ✅ Checklist de Implementación

- [ ] Crear HTTP API en API Gateway
- [ ] Configurar integration con EC2 MS5
- [ ] Configurar route `/{proxy+}`
- [ ] Configurar stage (prod)
- [ ] Configurar CORS
- [ ] Obtener Invoke URL
- [ ] Probar health check
- [ ] Probar endpoints de analytics
- [ ] Configurar variable en Amplify
- [ ] Redesplegar en Amplify
- [ ] Probar Analytics en el navegador
- [ ] Verificar en browser console (F12)

## 🔗 URLs Importantes

- **API Gateway Console:** https://console.aws.amazon.com/apigateway/
- **Amplify Console:** https://console.aws.amazon.com/amplify/
- **CloudWatch Logs:** https://console.aws.amazon.com/cloudwatch/
- **EC2 MS5:** http://54.196.248.70:8000
- **API Gateway URL:** https://[TU-ID].execute-api.us-east-1.amazonaws.com
- **Amplify App:** https://main.[TU-ID].amplifyapp.com

---

**Última actualización:** 2025-10-06  
**Status:** ✅ API Gateway configurado y funcionando
