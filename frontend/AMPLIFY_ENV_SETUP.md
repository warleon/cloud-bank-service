# Configuración de Variables de Entorno en AWS Amplify

## Variables necesarias para Analytics (MS5)

Para que la sección Analytics funcione correctamente, necesitas configurar la variable de entorno `REACT_APP_MS5_URL` en AWS Amplify.

## Pasos para configurar en Amplify Console

### 1. Acceder a Amplify Console
- Ve a la consola de AWS Amplify: https://console.aws.amazon.com/amplify/
- Selecciona tu aplicación `cloud-bank-app`

### 2. Agregar Variables de Entorno
1. En el menú lateral izquierdo, haz clic en **"Environment variables"** (Variables de entorno)
2. Haz clic en el botón **"Manage variables"** (Administrar variables)
3. Haz clic en **"Add variable"** (Agregar variable)

### 3. Configurar REACT_APP_MS5_URL

**Opción 1: Usando IP pública de EC2 MS5**
```
Variable: REACT_APP_MS5_URL
Value: http://54.196.248.70:8000
```

**Ejemplo (tu configuración actual):**
```
REACT_APP_MS5_URL=http://54.196.248.70:8000
```

**Opción 2: Usando API Gateway (recomendado para producción)**
```
Variable: REACT_APP_MS5_URL
Value: https://tu-api-gateway.execute-api.us-east-1.amazonaws.com/prod
```

### 4. Guardar y Redesplegar
1. Haz clic en **"Save"** (Guardar)
2. Ve a la pestaña **"Deployments"** (Despliegues)
3. Haz clic en **"Redeploy this version"** (Redesplegar esta versión)
   - O espera a que el próximo push a GitHub dispare un nuevo deploy automático

### 5. Verificar Configuración
Una vez completado el despliegue:
1. Abre tu aplicación en el navegador
2. Navega a la sección **📊 Analytics**
3. Abre la consola del navegador (F12) → pestaña Network
4. Verifica que las peticiones se hagan a la URL correcta de MS5

## Notas Importantes

### ⚠️ CORS (Cross-Origin Resource Sharing)
Si estás usando la IP directa de EC2, asegúrate de que `api-consultas` tenga CORS configurado correctamente. En `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominio de Amplify
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 🔒 Seguridad con API Gateway (Recomendado)
Para producción, es mejor usar API Gateway:

1. **Crear HTTP API en API Gateway:**
   - Tipo: HTTP API
   - Integration: HTTP Proxy
   - Endpoint: `http://IP_PRIVADA_EC2_MS5:8000/{proxy+}`

2. **Configurar CORS en API Gateway:**
   - Permitir origen: `https://tu-app.amplifyapp.com`
   - Métodos: GET, POST, OPTIONS
   - Headers: Content-Type, Authorization

3. **Usar la URL de API Gateway en Amplify:**
   ```
   REACT_APP_MS5_URL=https://abc123.execute-api.us-east-1.amazonaws.com
   ```

### 🔄 Variables de Entorno Actuales

El frontend ya tiene configuradas estas variables:

```javascript
// src/api.js
const API_ENDPOINTS = {
  clientes: process.env.REACT_APP_MS1_URL || 'http://localhost:5000',
  cuentas: process.env.REACT_APP_MS2_URL || 'http://localhost:3000',
  transacciones: process.env.REACT_APP_MS4_URL || 'http://localhost:8080',
  analytics: process.env.REACT_APP_MS5_URL || 'http://localhost:8000'
};
```

### 📊 Endpoints de Analytics Disponibles

Una vez configurado, la sección Analytics consumirá estos endpoints:

- `GET /api/dashboard` - Dashboard ejecutivo con 6 métricas
- `GET /api/cuentas/resumen` - Resumen de cuentas por tipo
- `GET /api/transacciones/resumen` - Resumen de transacciones por tipo
- `GET /api/analisis/clientes-vip` - Top 10 clientes VIP

### ⏱️ Timeouts
Las consultas a Athena pueden tomar 5-10 segundos. El frontend tiene un timeout de 30 segundos configurado:

```javascript
export const analyticsAPI = axios.create({
  baseURL: API_ENDPOINTS.analytics,
  timeout: 30000, // 30 segundos para queries de Athena
  headers: { 'Content-Type': 'application/json' }
});
```

## Troubleshooting

### Error: Network Error
- Verifica que EC2 MS5 esté corriendo
- Verifica Security Group permita puerto 8000
- Verifica CORS configurado correctamente

### Error: Timeout
- Las queries de Athena pueden ser lentas la primera vez
- Verifica logs de api-consultas: `docker logs ms5-api-consultas-1`
- Aumenta timeout si es necesario

### Error: 404 Not Found
- Verifica que la URL en `REACT_APP_MS5_URL` sea correcta
- Verifica que api-consultas esté corriendo: `curl http://IP:8000/health`

### No hay datos en Analytics
- Verifica que el ingester haya corrido exitosamente
- Verifica que Glue Crawlers hayan catalogado las tablas
- Ejecuta una query en Athena Console para verificar datos
