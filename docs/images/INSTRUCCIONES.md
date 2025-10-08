# INSTRUCCIONES PARA GENERAR DIAGRAMAS

Usar https://mermaid.live/ para convertir los siguientes códigos Mermaid a imágenes PNG.

---

## DIAGRAMA 1: Entidad-Relación - PostgreSQL (MS1)

**Archivo:** `er-postgresql.png`

```mermaid
erDiagram
    CLIENTES {
        SERIAL id PK
        VARCHAR(100) nombre
        VARCHAR(100) apellido
        VARCHAR(150) email UK
        VARCHAR(20) telefono
        VARCHAR(20) tipo_documento
        VARCHAR(50) numero_documento UK
        DATE fecha_nacimiento
        TEXT direccion
        VARCHAR(20) estado
        TIMESTAMP fecha_registro
    }
```

---

## DIAGRAMA 2: Entidad-Relación - MySQL (MS2)

**Archivo:** `er-mysql.png`

```mermaid
erDiagram
    CLIENTES ||--o{ CUENTAS : "tiene"
    
    CLIENTES {
        INT id PK
        VARCHAR nombre
        VARCHAR apellido
        VARCHAR email UK
    }
    
    CUENTAS {
        INT id PK
        INT cliente_id FK
        VARCHAR(20) numero_cuenta UK
        VARCHAR(50) tipo_cuenta
        VARCHAR(3) moneda
        DECIMAL(15_2) saldo
        VARCHAR(20) estado
        TIMESTAMP fecha_apertura
    }
```

---

## DIAGRAMA 3: Flujo MS1 (Gestión de Clientes)

**Archivo:** `flujo-ms1.png`

```mermaid
flowchart TD
    Start([Cliente hace petición]) --> API[API Gateway MS1<br/>FastAPI - Puerto 8001]
    API --> Method{Método HTTP}
    
    Method -->|GET /clientes| List[Listar todos<br/>los clientes]
    Method -->|GET /clientes/:id| Get[Obtener cliente<br/>por ID]
    Method -->|POST /clientes| Create[Crear nuevo<br/>cliente]
    Method -->|PUT /clientes/:id| Update[Actualizar<br/>cliente]
    Method -->|DELETE /clientes/:id| Delete[Eliminar<br/>cliente]
    
    List --> DB[(PostgreSQL<br/>clientes)]
    Get --> DB
    Create --> Validate[Validar datos<br/>email único<br/>documento único]
    Validate --> DB
    Update --> DB
    Delete --> DB
    
    DB --> Response[Respuesta JSON]
    Response --> End([Respuesta al cliente])
    
    style API fill:#3776ab
    style DB fill:#336791
    style Validate fill:#ffd700
```

---

## DIAGRAMA 4: Flujo MS2 (Gestión de Cuentas)

**Archivo:** `flujo-ms2.png`

```mermaid
flowchart TD
    Start([Cliente hace petición]) --> API[API Gateway MS2<br/>Express - Puerto 8002]
    API --> Method{Método HTTP}
    
    Method -->|GET /cuentas| List[Listar todas<br/>las cuentas]
    Method -->|GET /cuentas/:id| Get[Obtener cuenta<br/>por ID]
    Method -->|GET /cuentas/cliente/:id| GetByClient[Obtener cuentas<br/>por cliente_id]
    Method -->|POST /cuentas| Create[Crear nueva<br/>cuenta]
    Method -->|PUT /cuentas/:id/saldo| UpdateBalance[Actualizar<br/>saldo]
    
    List --> DB[(MySQL<br/>cuentas)]
    Get --> DB
    GetByClient --> DB
    Create --> Validate[Validar datos<br/>numero_cuenta único<br/>cliente_id existe]
    Validate -->|Verificar cliente| MS1[MS1: GET /clientes/:id]
    MS1 --> DB
    UpdateBalance --> DB
    
    DB --> Response[Respuesta JSON]
    Response --> End([Respuesta al cliente])
    
    style API fill:#339933
    style DB fill:#4479a1
    style MS1 fill:#3776ab
    style Validate fill:#ffd700
```

---

## DIAGRAMA 5: Flujo MS3 (API Agregador)

**Archivo:** `flujo-ms3.png`

```mermaid
flowchart TD
    Start([Cliente hace petición]) --> API[API Gateway MS3<br/>FastAPI - Puerto 8003]
    API --> Method{Endpoint}
    
    Method -->|GET /cliente/:id/completo| Profile[Perfil completo<br/>del cliente]
    
    Profile --> Parallel{Llamadas paralelas}
    
    Parallel --> MS1[MS1: GET /clientes/:id<br/>Datos personales]
    Parallel --> MS2[MS2: GET /cuentas/cliente/:id<br/>Cuentas bancarias]
    Parallel --> MS4[MS4: GET /transacciones/:cuenta_id<br/>Historial transacciones]
    
    MS1 --> Aggregate[Agregar respuestas<br/>en un solo JSON]
    MS2 --> Aggregate
    MS4 --> Aggregate
    
    Aggregate --> Cache{Cachear<br/>resultado?}
    Cache -->|Sí| Redis[(Redis Cache<br/>5 min TTL)]
    Cache -->|No| Response[Respuesta JSON<br/>unificada]
    Redis --> Response
    
    Response --> End([Respuesta al cliente])
    
    style API fill:#3776ab
    style MS1 fill:#3776ab
    style MS2 fill:#339933
    style MS4 fill:#f89820
    style Aggregate fill:#ffd700
    style Redis fill:#dc382d
```

---

## DIAGRAMA 6: Flujo MS4 (Transacciones)

**Archivo:** `flujo-ms4.png`

```mermaid
flowchart TD
    Start([Cliente hace petición]) --> API[API Gateway MS4<br/>Spring Boot - Puerto 8004]
    API --> Method{Método HTTP}
    
    Method -->|GET /transacciones| List[Listar todas<br/>las transacciones]
    Method -->|GET /transacciones/:id| Get[Obtener transacción<br/>por ID]
    Method -->|GET /transacciones/cuenta/:id| GetByAccount[Obtener por<br/>cuenta_id]
    Method -->|POST /transacciones| Create[Crear nueva<br/>transacción]
    
    List --> DB[(MongoDB<br/>transacciones)]
    Get --> DB
    GetByAccount --> DB
    
    Create --> ValidateTx[Validar transacción<br/>tipo, monto, cuenta]
    ValidateTx -->|Verificar cuenta| MS2[MS2: GET /cuentas/:id]
    MS2 --> CheckBalance{Tipo de<br/>transacción?}
    
    CheckBalance -->|RETIRO| Validate[Validar saldo<br/>suficiente]
    CheckBalance -->|DEPOSITO| Process[Procesar<br/>transacción]
    CheckBalance -->|TRANSFERENCIA| Validate
    
    Validate -->|Saldo OK| Process
    Validate -->|Saldo insuficiente| Error[Error 400<br/>Saldo insuficiente]
    
    Process --> UpdateMS2[MS2: PUT /cuentas/:id/saldo<br/>Actualizar saldo]
    UpdateMS2 --> DB
    
    DB --> Response[Respuesta JSON]
    Error --> Response
    Response --> End([Respuesta al cliente])
    
    style API fill:#f89820
    style DB fill:#47a248
    style MS2 fill:#339933
    style ValidateTx fill:#ffd700
    style Error fill:#ff0000
```

---

## DIAGRAMA 7: Flujo MS5 (Data Lake & Analytics)

**Archivo:** `flujo-ms5.png`

```mermaid
flowchart TD
    Start([Proceso Automático]) --> Ingester[Datalake Ingester<br/>Python Script]
    
    Ingester --> Parallel{Extrae datos}
    
    Parallel --> MS1[MS1: GET /clientes<br/>20k registros]
    Parallel --> MS2[MS2: GET /cuentas<br/>20k registros]
    Parallel --> MS4[MS4: GET /transacciones<br/>20k registros]
    
    MS1 --> Transform[Transformar a<br/>formato Parquet]
    MS2 --> Transform
    MS4 --> Transform
    
    Transform --> S3[(AWS S3<br/>datalake-raw/<br/>60k+ registros)]
    
    S3 --> Glue[AWS Glue Crawler<br/>Detectar esquema]
    Glue --> Catalog[(AWS Glue<br/>Data Catalog)]
    
    Catalog --> Query([Usuario consulta<br/>API MS5])
    Query --> API[API Consultas<br/>FastAPI - Puerto 8005]
    
    API --> Athena{AWS Athena<br/>SQL Queries}
    
    Athena -->|Query 1| Q1[Total clientes<br/>por estado]
    Athena -->|Query 2| Q2[Top 10 cuentas<br/>mayor saldo]
    Athena -->|Query 3| Q3[Volumen transacciones<br/>por tipo]
    Athena -->|Query 4| Q4[Análisis<br/>por moneda]
    
    Q1 --> S3
    Q2 --> S3
    Q3 --> S3
    Q4 --> S3
    
    S3 --> Response[Respuesta JSON<br/>resultados analytics]
    Response --> End([Respuesta al cliente])
    
    style Ingester fill:#3776ab
    style S3 fill:#ff9900
    style Glue fill:#ff9900
    style Catalog fill:#ff9900
    style Athena fill:#ff9900
    style API fill:#3776ab
```

---

## DIAGRAMA 8: Integración Completa entre Microservicios

**Archivo:** `integracion-completa.png`

```mermaid
flowchart TB
    Client([Cliente Frontend<br/>React]) --> ALB[AWS Application<br/>Load Balancer]
    
    ALB --> MS1[MS1: Clientes<br/>Python FastAPI<br/>:8001]
    ALB --> MS2[MS2: Cuentas<br/>Node Express<br/>:8002]
    ALB --> MS3[MS3: Agregador<br/>Python FastAPI<br/>:8003]
    ALB --> MS4[MS4: Transacciones<br/>Java Spring<br/>:8004]
    ALB --> MS5[MS5: Analytics<br/>Python FastAPI<br/>:8005]
    
    MS1 --> DB1[(PostgreSQL<br/>clientes<br/>20k registros)]
    MS2 --> DB2[(MySQL<br/>cuentas<br/>20k registros)]
    MS4 --> DB3[(MongoDB<br/>transacciones<br/>20k registros)]
    
    MS3 -.->|GET /clientes/:id| MS1
    MS3 -.->|GET /cuentas/cliente/:id| MS2
    MS3 -.->|GET /transacciones/cuenta/:id| MS4
    
    MS4 -.->|GET /cuentas/:id| MS2
    MS4 -.->|PUT /cuentas/:id/saldo| MS2
    
    MS5 --> Ingester[Ingester Process]
    Ingester -.->|Extract| MS1
    Ingester -.->|Extract| MS2
    Ingester -.->|Extract| MS4
    
    Ingester --> S3[(AWS S3<br/>Data Lake<br/>60k+ registros)]
    S3 --> Athena[AWS Athena]
    MS5 --> Athena
    
    style Client fill:#61dafb
    style ALB fill:#ff4f00
    style MS1 fill:#3776ab
    style MS2 fill:#339933
    style MS3 fill:#3776ab
    style MS4 fill:#f89820
    style MS5 fill:#3776ab
    style DB1 fill:#336791
    style DB2 fill:#4479a1
    style DB3 fill:#47a248
    style S3 fill:#ff9900
    style Athena fill:#ff9900
```

---

## RESUMEN DE ARCHIVOS A GENERAR:

1. ✅ `er-postgresql.png` - Entidad-Relación PostgreSQL (MS1)
2. ✅ `er-mysql.png` - Entidad-Relación MySQL (MS2)
3. ✅ `flujo-ms1.png` - Flujo MS1 (Clientes)
4. ✅ `flujo-ms2.png` - Flujo MS2 (Cuentas)
5. ✅ `flujo-ms3.png` - Flujo MS3 (Agregador)
6. ✅ `flujo-ms4.png` - Flujo MS4 (Transacciones)
7. ✅ `flujo-ms5.png` - Flujo MS5 (Data Lake)
8. ✅ `integracion-completa.png` - Integración completa sistema

**Total: 8 diagramas**

---

## INSTRUCCIONES DE USO:

1. Ir a https://mermaid.live/
2. Copiar el código Mermaid de cada diagrama
3. Pegar en el editor
4. Ajustar zoom si es necesario
5. Descargar como PNG con el nombre indicado
6. Guardar en `docs/images/`
7. Confirmar que tienes los 8 archivos PNG