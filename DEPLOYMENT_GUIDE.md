# Guía Rápida de Despliegue - Cloud Bank

## 🚀 Resumen Ejecutivo

Este documento te guía paso a paso para desplegar el sistema bancario completo.

---

## 📋 Checklist Pre-Despliegue

- [ ] Cuenta de AWS activa
- [ ] 3 instancias EC2 (Ubuntu 22.04) lanzadas
- [ ] Key pair (.pem) descargada
- [ ] Security Groups configurados
- [ ] Git instalado localmente
- [ ] Acceso SSH a las instancias

---

## 🔧 PASO 1: Configurar Instancias EC2

### Lanzar 3 Instancias EC2

**Instancia 1 - MS1 (Clientes)**
```
- Name: cloud-bank-ms1
- AMI: Ubuntu Server 22.04 LTS
- Instance Type: t2.small
- Storage: 20 GB
- Security Group: cloud-bank-ms1-sg
  - Inbound: SSH (22), HTTP (8001), PostgreSQL (5432)
```

**Instancia 2 - MS2 (Cuentas)**
```
- Name: cloud-bank-ms2
- AMI: Ubuntu Server 22.04 LTS
- Instance Type: t2.small
- Storage: 20 GB
- Security Group: cloud-bank-ms2-sg
  - Inbound: SSH (22), HTTP (8002), MySQL (3306)
```

**Instancia 3 - MS4 (Transacciones)**
```
- Name: cloud-bank-ms4
- AMI: Ubuntu Server 22.04 LTS
- Instance Type: t2.medium (Java requiere más recursos)
- Storage: 20 GB
- Security Group: cloud-bank-ms4-sg
  - Inbound: SSH (22), HTTP (8004), MongoDB (27017)
```

### Anotar IPs Públicas

```
MS1 IP: _________________
MS2 IP: _________________
MS4 IP: _________________
```

---

## 🐳 PASO 2: Instalar Docker en Cada Instancia

**Ejecutar en CADA una de las 3 instancias**:

```bash
# Conectar a EC2
ssh -i tu-key.pem ubuntu@<IP-INSTANCIA>

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
sudo apt install -y docker.io docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker ubuntu

# Habilitar Docker al inicio
sudo systemctl enable docker
sudo systemctl start docker

# Verificar instalación
docker --version
docker-compose --version

# IMPORTANTE: Cerrar sesión y reconectar
exit
ssh -i tu-key.pem ubuntu@<IP-INSTANCIA>

# Verificar que docker funciona sin sudo
docker ps
```

---

## 📦 PASO 3: Desplegar Microservicios

### MS1 - Clientes (Instancia 1)

```bash
# Conectar
ssh -i tu-key.pem ubuntu@<MS1-IP>

# Clonar repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service/ms1

# Levantar servicios
docker-compose up -d

# Ver logs (Ctrl+C para salir)
docker-compose logs -f

# Verificar contenedores
docker-compose ps

# Probar API
curl http://localhost:8001/
curl http://localhost:8001/clientes
```

**Resultado esperado**: 2 contenedores corriendo (postgres-clientes-db, api-clientes)

---

### MS2 - Cuentas (Instancia 2)

```bash
# Conectar
ssh -i tu-key.pem ubuntu@<MS2-IP>

# Clonar repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service/ms2

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Verificar contenedores
docker-compose ps

# Probar API
curl http://localhost:8002/
curl http://localhost:8002/cuentas
```

**Resultado esperado**: 2 contenedores corriendo (mysql-cuentas-db, api-cuentas)

---

### MS4 - Transacciones (Instancia 3)

```bash
# Conectar
ssh -i tu-key.pem ubuntu@<MS4-IP>

# Clonar repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service/ms4

# Levantar servicios (IMPORTANTE: build puede tomar 3-5 minutos)
docker-compose up -d

# Ver logs (esperar a que Spring Boot inicie)
docker-compose logs -f api-transacciones

# Esperar mensaje: "Started TransaccionesApplication"

# Verificar contenedores
docker-compose ps

# Probar API
curl http://localhost:8004/
curl http://localhost:8004/transacciones
```

**Resultado esperado**: 2 contenedores corriendo (mongo-transacciones-db, api-transacciones)

---

## 🌐 PASO 4: Probar APIs desde Internet

Desde tu navegador o terminal local:

```bash
# MS1 - Clientes
curl http://<MS1-IP>:8001/clientes

# MS2 - Cuentas
curl http://<MS2-IP>:8002/cuentas

# MS4 - Transacciones
curl http://<MS4-IP>:8004/transacciones
```

**Si no funcionan**: Revisar Security Groups en AWS Console.

---

## 🎨 PASO 5: Desplegar Frontend en AWS Amplify

### Opción A: Desde AWS Console (Recomendado)

1. **Ir a AWS Amplify Console**
   - Servicios → Amplify → Get Started

2. **Conectar Repositorio**
   - Clic en "Host web app"
   - Seleccionar "GitHub"
   - Autorizar acceso
   - Seleccionar: `cloud-bank-service`
   - Branch: `main`

3. **Configurar Build Settings**
   ```yaml
   Base directory: frontend
   Build command: npm run build
   Build output directory: build
   ```

4. **Agregar Variables de Entorno**
   ```
   REACT_APP_MS1_URL = http://<MS1-IP>:8001
   REACT_APP_MS2_URL = http://<MS2-IP>:8002
   REACT_APP_MS4_URL = http://<MS4-IP>:8004
   ```
   ⚠️ **IMPORTANTE**: Reemplaza `<MS1-IP>`, `<MS2-IP>`, `<MS4-IP>` con las IPs reales.

5. **Deploy**
   - Clic en "Save and deploy"
   - Esperar 5-7 minutos
   - Copiar URL de Amplify

### Opción B: Desde CLI

```bash
# Instalar Amplify CLI
npm install -g @aws-amplify/cli

# Configurar
amplify configure

# Inicializar
cd frontend
amplify init

# Agregar hosting
amplify add hosting

# Publicar
amplify publish
```

---

## ✅ PASO 6: Verificación Final

### Test End-to-End

1. **Abrir URL de Amplify en navegador**

2. **Módulo Clientes**
   - Clic en "👤 Clientes"
   - Registrar un nuevo cliente:
     ```
     Nombre: Juan
     Apellido: Pérez
     Email: juan.perez@test.com
     Teléfono: 999888777
     Tipo Doc: DNI
     Número: 12345678
     ```
   - Verificar que aparece en la lista
   - **Anotar el cliente_id** (aparece en la card)

3. **Módulo Cuentas**
   - Clic en "💳 Cuentas"
   - Crear cuenta:
     ```
     ID Cliente: [el que anotaste]
     Tipo Cuenta: Cuenta Sueldo
     Saldo: 1000
     Moneda: PEN
     ```
   - Verificar que aparece en la lista
   - **Anotar el cuenta_id y numero_cuenta**

4. **Módulo Transacciones**
   - Clic en "💸 Transacciones"
   - Crear transacción:
     ```
     Tipo: DEPOSITO
     ID Cuenta Destino: [el que anotaste]
     Monto: 500
     Moneda: PEN
     Descripción: Depósito de prueba
     ```
   - Verificar que aparece en la lista
   - Estado debe ser "PENDIENTE"

5. **Verificar en APIs directamente**
   ```bash
   # Ver cliente creado
   curl http://<MS1-IP>:8001/clientes
   
   # Ver cuenta creada
   curl http://<MS2-IP>:8002/cuentas
   
   # Ver transacción creada
   curl http://<MS4-IP>:8004/transacciones
   ```

---

## 🐛 Troubleshooting

### Problema: Frontend no se conecta a APIs

**Síntomas**: Error de red al crear cliente/cuenta/transacción

**Soluciones**:
1. Verificar variables de entorno en Amplify
2. Confirmar Security Groups permiten HTTP en puertos 8001, 8002, 8004
3. Probar APIs directamente con curl desde tu máquina
4. Revisar que las instancias EC2 estén corriendo

### Problema: Docker no funciona sin sudo

**Solución**:
```bash
# Agregar usuario al grupo
sudo usermod -aG docker ubuntu

# Reiniciar sesión (IMPORTANTE)
exit
ssh -i tu-key.pem ubuntu@<IP>

# Verificar
docker ps
```

### Problema: MS4 (Java) no inicia

**Síntomas**: Contenedor api-transacciones se reinicia constantemente

**Soluciones**:
1. Ver logs: `docker-compose logs -f api-transacciones`
2. Verificar que la instancia sea t2.medium (Java requiere RAM)
3. Esperar más tiempo (build inicial toma 3-5 minutos)
4. Verificar memoria: `free -h`

### Problema: Error de CORS en Frontend

**Síntomas**: CORS policy blocked request

**Solución**:
- Todas las APIs ya tienen CORS habilitado
- Verificar que las URLs en variables de entorno sean HTTP (no HTTPS)
- Confirmar que las IPs sean públicas (no privadas)

### Problema: Base de datos no inicia

**Síntomas**: API no se conecta a DB

**Solución**:
```bash
# Ver logs de la base de datos
docker-compose logs -f postgres-clientes-db  # MS1
docker-compose logs -f mysql-cuentas-db      # MS2
docker-compose logs -f mongo-transacciones-db # MS4

# Reiniciar servicios
docker-compose restart
```

---

## 📊 Monitoreo

### Ver Estado de Contenedores

```bash
# En cada instancia
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver uso de recursos
docker stats
```

### Endpoints de Health Check

```bash
# MS1
curl http://<MS1-IP>:8001/health

# MS2
curl http://<MS2-IP>:8002/health

# MS4
curl http://<MS4-IP>:8004/health
```

---

## 🔄 Actualizar Servicios

Si haces cambios en el código:

```bash
# Pull cambios
cd cloud-bank-service
git pull origin main

# Rebuild y restart
cd ms1  # o ms2, ms4
docker-compose up -d --build

# Ver logs
docker-compose logs -f
```

---

## 🛑 Detener Servicios

```bash
# Detener pero mantener datos
docker-compose stop

# Detener y eliminar contenedores (mantiene volúmenes)
docker-compose down

# Detener y eliminar TODO (incluyendo datos)
docker-compose down -v
```

---

## 💰 Costos Estimados AWS

**Instancias EC2** (24/7 por mes):
- 2 x t2.small: ~$34/mes
- 1 x t2.medium: ~$68/mes
- **Total**: ~$136/mes

**AWS Amplify**:
- Build: $0.01 por minuto
- Hosting: Gratis (hasta 1000 solicitudes/mes)
- **Estimado**: $2-5/mes

**Total mensual**: ~$140/mes

💡 **Tip**: Detén las instancias cuando no las uses para ahorrar costos.

---

## 🎓 Próximos Pasos

1. **Integrar con MS5 (DataLake)**
   - Ver guía en `m5/README.md`

2. **Implementar Autenticación**
   - AWS Cognito
   - JWT tokens

3. **Agregar Load Balancers**
   - Application Load Balancer para cada MS

4. **Implementar CI/CD**
   - GitHub Actions
   - AWS CodePipeline

5. **Monitoreo Avanzado**
   - CloudWatch Dashboards
   - Alertas SNS

---

## 📞 Soporte

Si tienes dudas:
1. Revisa este documento
2. Consulta READMEs individuales de cada MS
3. Revisa logs: `docker-compose logs -f`

---

**¡Feliz despliegue! 🚀**
