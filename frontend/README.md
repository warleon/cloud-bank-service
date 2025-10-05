# Frontend - Cloud Bank

Aplicación web React para gestionar el sistema bancario.

## 🏗️ Arquitectura

- **Framework**: React 18
- **Librería HTTP**: Axios
- **Despliegue**: AWS Amplify
- **Comunicación**: REST APIs con MS1, MS2, MS4

## 🚀 Despliegue en AWS Amplify

### Opción 1: Desde GitHub (Recomendado)

1. **Push del código a GitHub**
```bash
# Desde tu máquina local
cd cloud-bank-service
git add .
git commit -m "Add frontend"
git push origin main
```

2. **Configurar AWS Amplify**
```
a) Ir a AWS Amplify Console
b) Clic en "New app" → "Host web app"
c) Seleccionar "GitHub"
d) Autorizar acceso a tu repositorio
e) Seleccionar: cloud-bank-service
f) Build settings:
   - Base directory: frontend
   - Build command: npm run build
   - Build output directory: build
g) Agregar variables de entorno:
   - REACT_APP_MS1_URL: http://<EC2-MS1-IP>:8001
   - REACT_APP_MS2_URL: http://<EC2-MS2-IP>:8002
   - REACT_APP_MS4_URL: http://<EC2-MS4-IP>:8004
h) Clic en "Save and deploy"
```

3. **Esperar deployment (~5 minutos)**

### Opción 2: Despliegue Manual

```bash
# 1. Instalar Amplify CLI
npm install -g @aws-amplify/cli

# 2. Configurar credenciales
amplify configure

# 3. Inicializar proyecto
cd frontend
amplify init

# 4. Agregar hosting
amplify add hosting
# Seleccionar: Hosting with Amplify Console (Managed hosting)

# 5. Configurar variables de entorno en Amplify Console

# 6. Publicar
amplify publish
```

## 🔧 Configuración de Variables de Entorno

Crear archivo `.env` en la carpeta `frontend`:

```env
REACT_APP_MS1_URL=http://<EC2-MS1-IP>:8001
REACT_APP_MS2_URL=http://<EC2-MS2-IP>:8002
REACT_APP_MS4_URL=http://<EC2-MS4-IP>:8004
```

**IMPORTANTE**: Reemplaza `<EC2-MS1-IP>`, `<EC2-MS2-IP>`, `<EC2-MS4-IP>` con las IPs públicas de tus instancias EC2.

## 📝 Configuración de CORS en los Microservicios

Para que el frontend pueda comunicarse con los microservicios, asegúrate de que CORS esté habilitado en cada API:

**MS1 (Python/FastAPI)** - Ya configurado ✓
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**MS2 (Node.js/Express)** - Ya configurado ✓
```javascript
app.use(cors());
```

**MS4 (Java/Spring Boot)** - Ya configurado ✓
```java
@CrossOrigin(origins = "*")
```

## 🧪 Pruebas Locales

```bash
cd frontend

# Instalar dependencias
npm install

# Crear archivo .env con las URLs de las APIs
echo "REACT_APP_MS1_URL=http://localhost:8001" > .env
echo "REACT_APP_MS2_URL=http://localhost:8002" >> .env
echo "REACT_APP_MS4_URL=http://localhost:8004" >> .env

# Iniciar desarrollo
npm start

# Abrir http://localhost:3000
```

## 🌐 Funcionalidades

### 👤 Módulo Clientes
- Registrar nuevos clientes con documentos de identidad
- Ver lista de clientes registrados
- Información de contacto y estado

### 💳 Módulo Cuentas
- Crear cuentas bancarias para clientes existentes
- Seleccionar tipos de cuenta (Sueldo, Free, Premium, Ahorro)
- Ver saldos y estados de cuentas
- Soporte para múltiples monedas (PEN, USD, EUR)

### 💸 Módulo Transacciones
- Realizar depósitos
- Realizar retiros
- Transferencias entre cuentas
- Pagos de servicios
- Historial de transacciones

## 📦 Dependencias

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.0",
  "react-scripts": "5.0.1"
}
```

## 🔒 Security Groups de EC2

Para que el frontend pueda acceder a las APIs, los Security Groups de las instancias EC2 deben permitir:

```
Inbound Rules:
- Type: HTTP
- Protocol: TCP
- Port Range: 8001, 8002, 8004 (según el microservicio)
- Source: 0.0.0.0/0 (o la IP de Amplify si quieres más seguridad)
```

## 📱 Interfaz de Usuario

- **Diseño moderno**: Gradientes y efectos glassmorphism
- **Responsive**: Se adapta a móviles y tablets
- **Navegación intuitiva**: 3 módulos principales
- **Feedback visual**: Mensajes de éxito/error
- **Cards interactivas**: Hover effects y animaciones

## 🎨 Personalización

Para cambiar los colores del tema, edita `src/App.css`:

```css
/* Cambiar gradiente principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Cambiar color de badges */
.badge.activo {
  background: #d1fae5;
  color: #065f46;
}
```

## 📊 Build para Producción

```bash
npm run build
```

Esto genera la carpeta `build/` optimizada para producción.

## ⚠️ Troubleshooting

**Error de CORS**:
- Verifica que las APIs tengan CORS habilitado
- Confirma que las URLs en `.env` sean correctas

**No se conecta a las APIs**:
- Verifica que los Security Groups permitan tráfico HTTP
- Confirma que las instancias EC2 estén corriendo
- Prueba las APIs directamente con `curl` o Postman

**Build falla en Amplify**:
- Verifica que las variables de entorno estén configuradas
- Revisa los logs en Amplify Console
