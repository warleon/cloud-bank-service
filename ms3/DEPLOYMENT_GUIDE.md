# Guía de Despliegue - MS3 en EC2

## 📋 Requisitos Previos
- ✅ Instancia EC2 con Ubuntu
- ✅ Docker y Docker Compose instalados
- ✅ MS1, MS2 y MS4 desplegados y funcionando
- ✅ Puerto 6000 abierto en el Security Group

## 🚀 Pasos de Despliegue

### 1. Conectarse a la instancia EC2
```bash
ssh -i tu-key.pem ubuntu@<IP-EC2-MS3>
```

### 2. Instalar Docker (si no está instalado)
```bash
# Actualizar paquetes
sudo apt update

# Instalar Docker
sudo apt install -y docker.io docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker ubuntu

# Reiniciar sesión para aplicar cambios
exit
# Volver a conectarse
ssh -i tu-key.pem ubuntu@<IP-EC2-MS3>
```

### 3. Clonar el repositorio
```bash
cd ~
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service/ms3
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con las IPs correctas de tus EC2
nano .env
```

Contenido del `.env`:
```env
# URLs de otros microservicios (AJUSTAR con tus IPs)
MS1_URL=http://18.212.214.255:5000
MS2_URL=http://54.242.189.131:3000
MS4_URL=http://54.87.40.69:8080

# Configuración del servidor
PORT=6000
LOG_LEVEL=INFO
```

**Nota:** También debes editar el `docker-compose.yml` con las IPs correctas.

### 5. Levantar el contenedor
```bash
docker-compose up -d
```

### 6. Verificar que esté corriendo
```bash
# Ver logs
docker-compose logs -f

# Verificar contenedor
docker ps

# Salir de los logs: Ctrl+C
```

### 7. Probar el servicio

#### Health Check
```bash
curl http://localhost:6000/health
```

Respuesta esperada:
```json
{
  "ms3": "healthy",
  "timestamp": "2025-10-06T...",
  "microservicios": {
    "ms1": "connected",
    "ms2": "connected",
    "ms4": "connected"
  }
}
```

#### Obtener perfil completo de un cliente
```bash
curl http://localhost:6000/api/clientes/1/perfil-completo
```

#### Buscar clientes
```bash
curl "http://localhost:6000/api/clientes/buscar?q=Juan"
```

### 8. Abrir puerto en Security Group de AWS

1. Ve a EC2 → Security Groups
2. Selecciona el Security Group de tu instancia MS3
3. Agregar regla de entrada:
   - **Type:** Custom TCP
   - **Port:** 6000
   - **Source:** Anywhere IPv4 (0.0.0.0/0) o tu IP específica
   - **Description:** MS3 API

### 9. Probar desde tu máquina local
```bash
# Reemplaza con la IP pública de tu EC2
curl http://<IP-PUBLICA-EC2-MS3>:6000/health
```

## 🔄 Comandos de Mantenimiento

### Ver logs en tiempo real
```bash
cd ~/cloud-bank-service/ms3
docker-compose logs -f
```

### Reiniciar servicio
```bash
docker-compose restart
```

### Detener servicio
```bash
docker-compose down
```

### Actualizar código
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Ver estado del contenedor
```bash
docker ps
docker stats ms3-perfil-cliente
```

## 🐛 Troubleshooting

### Si no puede conectar con otros microservicios

1. **Verificar que MS1, MS2 y MS4 estén corriendo:**
```bash
curl http://18.212.214.255:5000/clientes
curl http://54.242.189.131:3000/cuentas
curl http://54.87.40.69:8080/transacciones
```

2. **Verificar Security Groups:**
   - MS1, MS2 y MS4 deben tener sus puertos abiertos
   - Asegúrate de que las instancias puedan comunicarse entre sí

3. **Ver logs del MS3:**
```bash
docker-compose logs -f ms3-perfil-cliente
```

### Si el puerto 6000 está ocupado
```bash
# Ver qué está usando el puerto
sudo lsof -i :6000

# Cambiar el puerto en docker-compose.yml
nano docker-compose.yml
# Cambiar "6000:6000" por "7000:6000" (por ejemplo)
```

### Si Docker no inicia
```bash
# Verificar status de Docker
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker

# Habilitar Docker al inicio
sudo systemctl enable docker
```

## 📊 Monitoreo

### Ver uso de recursos
```bash
docker stats ms3-perfil-cliente
```

### Ver logs de errores
```bash
docker-compose logs --tail=100 ms3-perfil-cliente | grep ERROR
```

## 🔒 Seguridad (Recomendaciones para Producción)

1. **Restringir CORS** en `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # Solo tu dominio
    ...
)
```

2. **Usar HTTPS** con certificado SSL/TLS

3. **Agregar autenticación** (JWT, API Keys, etc.)

4. **Limitar rate limiting** para evitar abuso

## 📝 Notas Importantes

⚠️ **Las IPs de AWS Academy cambian:** Si reinicias los EC2, deberás actualizar las IPs en el `.env` y reiniciar el contenedor.

⚠️ **Dependencias:** Este servicio NO funcionará si MS1, MS2 o MS4 están caídos.

⚠️ **Timeouts:** Los requests tienen timeout de 30 segundos. Si los otros MS son lentos, ajusta el valor en `main.py`.

## ✅ Checklist de Despliegue

- [ ] EC2 creada y accesible vía SSH
- [ ] Docker instalado
- [ ] Repositorio clonado
- [ ] Variables de entorno configuradas con IPs correctas
- [ ] Puerto 6000 abierto en Security Group
- [ ] Contenedor levantado (`docker-compose up -d`)
- [ ] Health check exitoso (`curl http://localhost:6000/health`)
- [ ] Endpoint funcional desde fuera (`curl http://<IP-PUBLICA>:6000/health`)
- [ ] MS1, MS2 y MS4 respondiendo correctamente

## 🎉 Resultado Final

Una vez desplegado, tendrás:
- **MS3 API** corriendo en `http://<IP-PUBLICA>:6000`
- **Endpoint principal:** `/api/clientes/{id}/perfil-completo`
- **Búsqueda:** `/api/clientes/buscar?q=Juan`
- **Health check:** `/health`

¡Listo para integrarlo con tu frontend! 🚀
