# 📚 Documentación Swagger UI - Cloud Bank Service

## ✅ URLs de Documentación de APIs

Todos los microservicios cuentan con documentación interactiva Swagger UI:

### **MS1 - Clientes (Python/FastAPI + PostgreSQL)**
- **Swagger UI**: http://54.167.116.254:8001/docs
- **OpenAPI JSON**: http://54.167.116.254:8001/openapi.json
- **Tecnología**: FastAPI (Swagger integrado)
- **Base de Datos**: PostgreSQL

### **MS2 - Cuentas (Node.js/Express + MySQL)**
- **Swagger UI**: http://54.242.68.197:8002/docs
- **Tecnología**: swagger-ui-express + swagger-jsdoc
- **Base de Datos**: MySQL

### **MS3 - Perfil Cliente 360° (Python/FastAPI - Sin BD)**
- **Swagger UI**: http://54.165.212.211:6000/docs
- **OpenAPI JSON**: http://54.165.212.211:6000/openapi.json
- **Tecnología**: FastAPI (Swagger integrado)
- **Arquitectura**: Agregador sin base de datos (consume MS1, MS2, MS4)

### **MS4 - Transacciones (Java/Spring Boot + MongoDB)**
- **Swagger UI**: http://52.90.2.132:8004/docs
- **OpenAPI JSON**: http://52.90.2.132:8004/api-docs
- **Tecnología**: springdoc-openapi
- **Base de Datos**: MongoDB

### **MS5 - Analytics (Python/FastAPI + AWS Athena)**
- **Swagger UI**: http://35.172.225.47:8000/docs
- **OpenAPI JSON**: http://35.172.225.47:8000/openapi.json
- **Tecnología**: FastAPI (Swagger integrado)
- **Base de Datos**: AWS Athena (DataLake)

---

## 📊 **Resumen de Tecnologías**

| Microservicio | Lenguaje | Framework | Base de Datos | Swagger |
|---------------|----------|-----------|---------------|---------|
| MS1 - Clientes | Python | FastAPI | PostgreSQL | ✅ Integrado |
| MS2 - Cuentas | Node.js | Express | MySQL | ✅ swagger-ui-express |
| MS3 - Perfil 360° | Python | FastAPI | N/A | ✅ Integrado |
| MS4 - Transacciones | Java | Spring Boot | MongoDB | ✅ springdoc-openapi |
| MS5 - Analytics | Python | FastAPI | AWS Athena | ✅ Integrado |

---

## 🚀 **Cómo usar Swagger UI**

1. **Accede a la URL** de cualquier microservicio (ver arriba).
2. **Explora los endpoints** disponibles organizados por tags.
3. **Prueba los endpoints** directamente desde la interfaz:
   - Click en el endpoint que desees probar.
   - Click en "Try it out".
   - Completa los parámetros requeridos.
   - Click en "Execute".
4. **Revisa las respuestas** con código de estado y datos.

---

## 🔧 **Actualizar después de cambios de IP**

Si las IPs públicas de EC2 cambian (después de detener/iniciar instancias), actualiza las URLs en este documento y en los clientes.

**Verificar IPs actuales:**
```bash
# Desde AWS Console → EC2 → Instances
# O desde tu terminal:
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`].Value|[0],PublicIpAddress]' --output table
```

---

## 📖 **Documentación adicional**

- **Arquitectura del sistema**: Ver `SUMMARY.md`
- **Guía de despliegue**: Ver `DEPLOYMENT_GUIDE.md`
- **Ejemplos de API**: Ver `API_EXAMPLES.md`

---

## ✅ **Cumplimiento de requisitos**

- ✅ 5 microservicios en Docker
- ✅ 3 lenguajes diferentes (Python, Node.js, Java)
- ✅ 3 bases de datos diferentes (PostgreSQL, MySQL, MongoDB + Athena)
- ✅ **Documentación Swagger UI en todas las APIs** 📚
- ✅ Repositorio público en GitHub

---

**Última actualización**: 7 de octubre de 2025
