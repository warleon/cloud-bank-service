# API Gateway para MS3 - Perfil Cliente 360°

## 🎯 Objetivo
Crear un API Gateway en AWS para MS3 que permita acceso público HTTPS con CORS configurado.

## 📋 Pasos de Configuración

### 1. Acceder a API Gateway Console
1. Ir a **AWS Console** → Buscar **API <Gateway**
2. Click en **Create API**
3. Seleccionar **HTTP API** (no REST API)
4. Click en **Build**

### 2. Configuración Inicial
**Paso 1: Create and configure integrations**
- **Integration type**: HTTP
- **URL endpoint**: `http://34.234.91.211:6000`
- **Method**: ANY
- **API name**: `ms3-perfil-cliente-api`
- **Description**: API Gateway para Perfil Cliente 360 (MS3)
- Click **Next**

**Paso 2: Configure routes**
- Mantener la ruta por defecto: `ANY /{proxy+}`
- Esto permite que todas las rutas pasen al backend
- Click **Next**

**Paso 3: Define stages**
- **Stage name**: `prod`
- **Auto-deploy**: ✅ (activado)
- Click **Next**

**Paso 4: Review and create**
- Revisar configuración
- Click **Create**

### 3. Configurar CORS
1. En el API recién creado, ir a **CORS**
2. Click **Configure**
3. Configurar:
   - **Access-Control-Allow-Origin**: `*` (o tu dominio específico de Amplify)
   - **Access-Control-Allow-Headers**: `*`
   - **Access-Control-Allow-Methods**: `GET, POST, PUT, DELETE, OPTIONS`
   - **Access-Control-Max-Age**: `86400`
4. Click **Save**

### 4. Obtener URL del API Gateway
1. Ir a **Stages** → **prod**
2. Copiar la **Invoke URL**
3. Ejemplo: `https://abc123def.execute-api.us-east-1.amazonaws.com/`

### 5. Probar el API Gateway
```bash
# Health check
curl https://TU_API_GATEWAY_URL/health

# Perfil completo
curl https://TU_API_GATEWAY_URL/api/clientes/1/perfil-completo

# Búsqueda
curl "https://TU_API_GATEWAY_URL/api/clientes/buscar?q=Juan"
```

### 6. Configurar en Amplify Frontend
1. Ir a **AWS Amplify** → Tu app
2. Click en **Environment variables**
3. Agregar:
   - **Key**: `REACT_APP_MS3_URL`
   - **Value**: `https://TU_API_GATEWAY_URL` (SIN barra final)
4. Click **Save**
5. Hacer **Redeploy** o esperar el próximo auto-deploy desde GitHub

## 🔧 Configuración Alternativa Específica

Si quieres mayor control, puedes configurar rutas específicas:

### Rutas Específicas
En lugar de `ANY /{proxy+}`, crear:
- `GET /health` → `http://34.234.91.211:6000/health`
- `GET /api/clientes/{id}/perfil-completo` → `http://34.234.91.211:6000/api/clientes/{id}/perfil-completo`
- `GET /api/clientes/buscar` → `http://34.234.91.211:6000/api/clientes/buscar`
- `GET /api/clientes/{id}/transacciones` → `http://34.234.91.211:6000/api/clientes/{id}/transacciones`

## 📊 Monitoreo
En API Gateway console:
- **Monitor**: Ver métricas de requests, latencia, errores
- **Logs**: Habilitar CloudWatch Logs para debugging

## 🔒 Seguridad (Opcional)
Para producción, considera:
- **Throttling**: Limitar requests por segundo
- **API Keys**: Requiere autenticación
- **WAF**: Firewall de aplicación web
- **Custom Domain**: Tu propio dominio personalizado

## 🌐 Arquitectura Final
```
Usuario Frontend (Amplify)
    ↓ HTTPS
API Gateway MS3
    ↓ HTTP
EC2 MS3 (34.234.91.211:6000)
    ↓ HTTP
MS1, MS2, MS4
```

## ✅ Verificación
Después de configurar:
1. ✅ Health check responde desde API Gateway
2. ✅ CORS headers presentes en respuestas
3. ✅ Frontend puede hacer requests sin CORS errors
4. ✅ Todos los endpoints funcionan a través del Gateway

## 📝 Notas Importantes
- La IP del EC2 (34.234.91.211) está hardcodeada en el backend. Si cambias de EC2, actualizar esta IP en API Gateway.
- API Gateway agrega ~10-50ms de latencia (aceptable).
- HTTP API es más barato y simple que REST API.
- Si el EC2 se detiene, el API Gateway devolverá 503 Service Unavailable.

## 🔄 Actualización del Frontend
Una vez configurado el API Gateway, el frontend usará automáticamente la URL del Gateway si está en `REACT_APP_MS3_URL`:
```javascript
// En api.js, ya está configurado:
perfilCliente: process.env.REACT_APP_MS3_URL || 'http://localhost:6000'
```

Con esto, el frontend de producción usará API Gateway, y el desarrollo local seguirá usando `localhost:6000`.
