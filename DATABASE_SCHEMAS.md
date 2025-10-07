# 📊 Diagramas y Estructuras de Datos - Cloud Bank Service

## 📐 Diagramas Entidad/Relación (SQL)

### **MS1 - Clientes (PostgreSQL)**

#### Diagrama ER

```
┌─────────────────────────────┐
│        CLIENTES             │
├─────────────────────────────┤
│ PK cliente_id (INTEGER)     │
│    nombre (VARCHAR 100)     │
│    apellido (VARCHAR 100)   │
│    email (VARCHAR 150) UK   │
│    telefono (VARCHAR 20)    │
│    fecha_registro (DATETIME)│
│    estado (VARCHAR 20)      │
└──────────┬──────────────────┘
           │
           │ 1:N
           │
┌──────────▼──────────────────┐
│  DOCUMENTOS_IDENTIDAD       │
├─────────────────────────────┤
│ PK documento_id (INTEGER)   │
│ FK cliente_id (INTEGER)     │
│    tipo_documento (VARCHAR) │
│    numero_documento (VARCHAR)│
│    fecha_emision (DATE)     │
│    fecha_vencimiento (DATE) │
└─────────────────────────────┘
```

#### Relaciones
- **1:N** - Un cliente puede tener múltiples documentos de identidad

#### Tablas SQL

**Tabla: clientes**
```sql
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo'
);
```

**Tabla: documentos_identidad**
```sql
CREATE TABLE documentos_identidad (
    documento_id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id) ON DELETE CASCADE,
    tipo_documento VARCHAR(50) NOT NULL,
    numero_documento VARCHAR(50) NOT NULL,
    fecha_emision DATE,
    fecha_vencimiento DATE
);
```

---

### **MS2 - Cuentas (MySQL)**

#### Diagrama ER

```
┌─────────────────────────────┐
│      TIPOS_CUENTA           │
├─────────────────────────────┤
│ PK tipo_cuenta_id (INT)     │
│    nombre (VARCHAR 100)     │
│    descripcion (TEXT)       │
│    estado (VARCHAR 20)      │
└──────────┬──────────────────┘
           │
           │ 1:N
           │
┌──────────▼──────────────────┐
│         CUENTAS             │
├─────────────────────────────┤
│ PK cuenta_id (INT)          │
│ FK cliente_id (INT)         │
│ FK tipo_cuenta_id (INT)     │
│    numero_cuenta (VARCHAR)  │
│    saldo (DECIMAL 15,2)     │
│    moneda (VARCHAR 3)       │
│    fecha_apertura (DATETIME)│
│    estado (VARCHAR 20)      │
└─────────────────────────────┘
```

#### Relaciones
- **1:N** - Un tipo de cuenta puede tener múltiples cuentas
- **N:1** - Múltiples cuentas pertenecen a un cliente (referencia externa a MS1)

#### Tablas SQL

**Tabla: tipos_cuenta**
```sql
CREATE TABLE tipos_cuenta (
    tipo_cuenta_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'activo'
);
```

**Tabla: cuentas**
```sql
CREATE TABLE cuentas (
    cuenta_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo_cuenta_id INT,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    saldo DECIMAL(15,2) DEFAULT 0.00,
    moneda VARCHAR(3) DEFAULT 'PEN',
    fecha_apertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activa',
    FOREIGN KEY (tipo_cuenta_id) REFERENCES tipos_cuenta(tipo_cuenta_id)
);
```

**Índices:**
```sql
CREATE INDEX idx_cliente_id ON cuentas(cliente_id);
CREATE INDEX idx_numero_cuenta ON cuentas(numero_cuenta);
```

---

## 📄 Estructuras JSON (NoSQL)

### **MS4 - Transacciones (MongoDB)**

#### Colección: `transacciones`

**Estructura del documento:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "transaccionId": "TRX-20251007-001234",
  "tipo": "DEPOSITO",
  "cuentaOrigenId": 1,
  "cuentaDestinoId": null,
  "monto": 1500.00,
  "moneda": "PEN",
  "descripcion": "Depósito en efectivo",
  "fecha": "2025-10-07T10:30:00.000Z",
  "estado": "completada",
  "metadata": {
    "canal": "cajero_automatico",
    "ubicacion": "Lima, Perú",
    "ip": "192.168.1.100"
  },
  "createdAt": "2025-10-07T10:30:00.000Z",
  "updatedAt": "2025-10-07T10:30:05.000Z"
}
```

**Campos:**

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `_id` | ObjectId | ID único de MongoDB | Sí (auto) |
| `transaccionId` | String | ID único legible (TRX-YYYYMMDD-NNNNNN) | Sí |
| `tipo` | String (Enum) | DEPOSITO, RETIRO, TRANSFERENCIA | Sí |
| `cuentaOrigenId` | Integer | ID de cuenta origen | Condicional |
| `cuentaDestinoId` | Integer | ID de cuenta destino | Condicional |
| `monto` | Double | Monto de la transacción | Sí |
| `moneda` | String | Código de moneda (PEN, USD) | Sí |
| `descripcion` | String | Descripción de la transacción | No |
| `fecha` | Date | Fecha y hora de la transacción | Sí |
| `estado` | String (Enum) | pendiente, completada, rechazada | Sí |
| `metadata` | Object | Información adicional | No |
| `createdAt` | Date | Fecha de creación del registro | Sí (auto) |
| `updatedAt` | Date | Fecha de última actualización | Sí (auto) |

**Enums:**
```json
{
  "tipo": ["DEPOSITO", "RETIRO", "TRANSFERENCIA"],
  "estado": ["pendiente", "completada", "rechazada"],
  "moneda": ["PEN", "USD", "EUR"]
}
```

**Validaciones MongoDB:**
```javascript
db.createCollection("transacciones", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["transaccionId", "tipo", "monto", "moneda", "fecha", "estado"],
      properties: {
        transaccionId: {
          bsonType: "string",
          pattern: "^TRX-[0-9]{8}-[0-9]{6}$"
        },
        tipo: {
          enum: ["DEPOSITO", "RETIRO", "TRANSFERENCIA"]
        },
        monto: {
          bsonType: "double",
          minimum: 0
        },
        moneda: {
          bsonType: "string",
          minLength: 3,
          maxLength: 3
        },
        estado: {
          enum: ["pendiente", "completada", "rechazada"]
        }
      }
    }
  }
});
```

**Índices MongoDB:**
```javascript
db.transacciones.createIndex({ "transaccionId": 1 }, { unique: true });
db.transacciones.createIndex({ "cuentaOrigenId": 1 });
db.transacciones.createIndex({ "cuentaDestinoId": 1 });
db.transacciones.createIndex({ "fecha": -1 });
db.transacciones.createIndex({ "tipo": 1 });
db.transacciones.createIndex({ "estado": 1 });
```

---

## 🔗 Relaciones entre Microservicios

```
┌─────────────┐
│    MS1      │
│  Clientes   │◄─────┐
└──────┬──────┘      │
       │             │
       │ cliente_id  │ cliente_id
       │             │
┌──────▼──────┐      │
│    MS2      │      │
│   Cuentas   │◄─────┼───────┐
└──────┬──────┘      │       │
       │             │       │
       │ cuenta_id   │       │ cuenta_id
       │             │       │
┌──────▼──────┐      │       │
│    MS4      │      │       │
│Transacciones│      │       │
└─────────────┘      │       │
                     │       │
┌─────────────┐      │       │
│    MS3      │──────┴───────┘
│ Perfil 360° │
│ (Agregador) │
└─────────────┘
```

### Notas sobre las relaciones:
- **MS1** guarda clientes con su `cliente_id`
- **MS2** referencia `cliente_id` de MS1 (sin FK física, solo lógica)
- **MS4** referencia `cuentaOrigenId` y `cuentaDestinoId` de MS2 (sin FK física)
- **MS3** consulta y agrega datos de MS1, MS2 y MS4 (sin base de datos propia)

---

## 📈 Resumen de Estructuras

| Microservicio | Base de Datos | Tablas/Colecciones | Relaciones |
|---------------|---------------|-------------------|------------|
| MS1 | PostgreSQL | 2 tablas | 1:N (clientes → documentos) |
| MS2 | MySQL | 2 tablas | 1:N (tipos_cuenta → cuentas) |
| MS4 | MongoDB | 1 colección | Referencias lógicas a MS2 |
| MS5 | AWS Athena | Tablas externas | DataLake S3 |

---

**Última actualización**: 7 de octubre de 2025
