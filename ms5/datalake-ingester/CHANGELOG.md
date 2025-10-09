# Changelog - DataLake Ingester

## [2.0.0] - 2025-10-09

### ✨ Nueva Funcionalidad: Auto-limpieza de S3

#### Cambios Realizados:
- **Agregado método `clean_s3_bucket()`** en `ingester.py`
  - Elimina automáticamente todos los objetos del bucket S3 antes de cada ingesta
  - Previene duplicados de múltiples ejecuciones del ingester
  - Usa paginación para manejar buckets con muchos objetos
  - Elimina en lote (hasta 1000 objetos por llamada) para eficiencia

- **Modificado `run_ingestion.py`**
  - Agregado `ingester.clean_s3_bucket()` en las 3 funciones de ingesta:
    - `ingest_postgresql_data()` - Limpia `raw-ms1-data-bgc`
    - `ingest_mysql_data()` - Limpia `raw-ms2-data-bgc`
    - `ingest_mongodb_data()` - Limpia `raw-ms4-data-bgc`

#### Beneficios:
✅ **Sin duplicados**: Cada ingesta reemplaza completamente los datos anteriores  
✅ **Queries más simples**: No necesitas DISTINCT en Athena  
✅ **Datos frescos**: Siempre trabajas con la última snapshot de las bases de datos  
✅ **Uso eficiente de S3**: No acumula datos históricos innecesarios  

#### Comportamiento:
```
🚀 Iniciando proceso de ingesta completo
============================================================
Iniciando ingesta desde PostgreSQL (MS1 - Clientes)
============================================================
🧹 Limpiando bucket S3: raw-ms1-data-bgc
✅ Bucket limpiado: 25 objetos eliminados de raw-ms1-data-bgc
Extrayendo tabla 'clientes'...
✅ Subidos 7 registros de clientes a S3 bucket: raw-ms1-data-bgc
```

#### Modo Continuo:
En modo `INGESTION_MODE=continuous`, el ingester:
1. Limpia los 3 buckets S3
2. Extrae datos frescos de las 3 bases de datos
3. Sube a S3 con particionamiento de fecha actual
4. Espera `INGESTION_INTERVAL` segundos
5. Repite el ciclo

Esto significa que **siempre tendrás solo la última versión de los datos** en S3.

#### Rollback (si necesitas deshacer):
Si por alguna razón necesitas mantener datos históricos en S3, simplemente comenta las líneas:
```python
# ingester.clean_s3_bucket()
```

En los 3 archivos de `run_ingestion.py`.

---

## Notas Técnicas

### Permisos IAM Requeridos:
El ingester necesita estos permisos S3:
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:PutObject",
    "s3:GetObject",
    "s3:ListBucket",
    "s3:DeleteObject"  // ← NUEVO
  ],
  "Resource": [
    "arn:aws:s3:::raw-ms1-data-bgc/*",
    "arn:aws:s3:::raw-ms2-data-bgc/*",
    "arn:aws:s3:::raw-ms4-data-bgc/*"
  ]
}
```

### Impacto en Athena:
- Las queries con filtros de fecha (`year/month/day`) funcionarán correctamente
- Solo habrá datos de la fecha de la última ingesta
- Glue Crawler debe ejecutarse después de cada ingesta para actualizar el catálogo

### Testing:
```bash
# Ejecutar ingesta manual
cd ~/cloud-bank-service/ms5/datalake-ingester
docker-compose run --rm datalake-ingester python run_ingestion.py

# Verificar limpieza
aws s3 ls s3://raw-ms1-data-bgc/ --recursive

# Debería mostrar solo archivos de la última ejecución
```
