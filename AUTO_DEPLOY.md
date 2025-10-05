# 🚀 Despliegue Automático con Reintentos

Este proyecto ahora incluye **reintentos automáticos** en todos los microservicios para garantizar que se conecten correctamente a sus bases de datos, incluso si las bases de datos tardan en inicializarse.

## 🔧 Mejoras Implementadas

### 1. **Reintentos en el Código**

#### MS1 (Python + PostgreSQL)
```python
def create_db_engine(retries=5, delay=5):
    """Crea la conexión a la base de datos con reintentos"""
    for i in range(retries):
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            print(f"✅ Conectado a PostgreSQL exitosamente")
            return engine
        except Exception as e:
            print(f"⚠️  Intento {i + 1}/{retries} - PostgreSQL no disponible aún...")
            time.sleep(delay)
```

- **5 reintentos** con **5 segundos** de espera entre cada intento
- Total: hasta **25 segundos** esperando a PostgreSQL

#### MS2 (Node.js + MySQL)
```javascript
async function initDB(retries = 5, delay = 5000) {
    for (let i = 0; i < retries; i++) {
        try {
            pool = mysql.createPool(dbConfig);
            const connection = await pool.getConnection();
            console.log('✅ Conectado a MySQL');
            return;
        } catch (error) {
            console.log(`⚠️  Intento ${i + 1}/${retries} - Reintentando...`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}
```

- **5 reintentos** con **5 segundos** de espera
- Total: hasta **25 segundos** esperando a MySQL

#### MS4 (Java + MongoDB)
```properties
spring.data.mongodb.uri=mongodb://admin:admin123@mongodb:27017/transacciones_db?authSource=admin&connectTimeoutMS=30000&socketTimeoutMS=30000&serverSelectionTimeoutMS=30000&retryWrites=true&retryReads=true
```

- **30 segundos** de timeout para conexión
- **Reintentos automáticos** habilitados en escrituras y lecturas

### 2. **Política de Restart en Docker Compose**

Todos los servicios de API ahora tienen `restart: on-failure`:

```yaml
api-clientes:
  restart: on-failure  # ← Reinicia automáticamente si falla
  depends_on:
    postgres-db:
      condition: service_healthy
```

**Comportamiento**:
- Si el contenedor falla (exit code != 0), Docker lo **reinicia automáticamente**
- Combinado con los reintentos en el código, garantiza que se conecte eventualmente

## 🎯 Script Maestro de Despliegue

### `deploy-all.sh`

Script bash que despliega **todos los microservicios automáticamente**:

```bash
chmod +x deploy-all.sh
./deploy-all.sh
```

**¿Qué hace?**
1. ✅ Verifica que Docker y Docker Compose estén instalados
2. 🚀 Despliega MS1 (Python + PostgreSQL)
3. 🚀 Despliega MS2 (Node.js + MySQL)
4. 🚀 Despliega MS4 (Java + MongoDB) - tarda 5-10 min por Maven
5. 📊 Muestra el estado de todos los servicios
6. 📋 Imprime URLs de acceso

### Uso en EC2

```bash
# Conectar a la instancia EC2
# Clonar el repositorio
git clone https://github.com/Br4yanGC/cloud-bank-service.git
cd cloud-bank-service

# Dar permisos de ejecución
chmod +x deploy-all.sh

# Ejecutar despliegue completo
./deploy-all.sh
```

**Salida esperada**:
```
================================================
🚀 DESPLIEGUE AUTOMÁTICO - CLOUD BANK SERVICES
================================================

✅ Docker y Docker Compose disponibles

================================================
📦 Desplegando MS1 - Gestión de Clientes
================================================
🔄 Deteniendo contenedores previos...
🚀 Iniciando servicios...
⏳ Esperando inicialización...
📊 Estado de contenedores:
✅ MS1 - Gestión de Clientes desplegado

================================================
📦 Desplegando MS2 - Gestión de Cuentas
================================================
...

================================================
✅ DESPLIEGUE COMPLETADO
================================================

📋 Servicios desplegados:

  🐍 MS1 - Clientes:      http://localhost:8001
  📊 Swagger MS1:         http://localhost:8001/docs
  
  🟢 MS2 - Cuentas:       http://localhost:8002
  
  ☕ MS4 - Transacciones: http://localhost:8004
```

## 🔍 Verificación Manual

Si quieres verificar manualmente cada servicio:

```bash
# MS1
cd ms1
docker-compose ps
docker-compose logs api-clientes

# MS2
cd ../ms2
docker-compose ps
docker-compose logs api-cuentas

# MS4
cd ../ms4
docker-compose ps
docker-compose logs api-transacciones
```

## 🧪 Pruebas de API

```bash
# MS1 - Clientes
curl http://localhost:8001/
curl http://localhost:8001/clientes

# MS2 - Cuentas
curl http://localhost:8002/
curl http://localhost:8002/cuentas

# MS4 - Transacciones
curl http://localhost:8004/
curl http://localhost:8004/transacciones
```

## 📝 Notas Importantes

### ⏱️ Tiempos de Despliegue

- **MS1** (Python): ~30-60 segundos
- **MS2** (Node.js): ~30-60 segundos
- **MS4** (Java): **5-10 minutos** (Maven descarga y compila)

### 🔄 ¿Por qué MS4 tarda tanto?

Maven necesita:
1. Descargar todas las dependencias de Spring Boot (~100 MB)
2. Compilar el código Java
3. Construir el archivo JAR
4. Iniciar Spring Boot

**Es normal**. Una vez construido, los reinicios son rápidos.

### 🛠️ Solución de Problemas

Si un servicio no arranca:

1. **Ver logs**:
   ```bash
   docker-compose logs -f <nombre-contenedor>
   ```

2. **Reintentar manualmente**:
   ```bash
   docker-compose restart <nombre-contenedor>
   ```

3. **Reconstruir desde cero**:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

## 🎉 Ventajas del Sistema de Reintentos

✅ **Despliegue automático sin intervención manual**  
✅ **Tolerante a latencias de inicialización de bases de datos**  
✅ **Ideal para CI/CD y orquestación automatizada**  
✅ **Logs claros indicando estado de reintentos**  
✅ **Compatible con Docker Swarm, Kubernetes, ECS**

---

**¿Preguntas?** Revisa el [README principal](./README.md) o los READMEs individuales de cada microservicio.
