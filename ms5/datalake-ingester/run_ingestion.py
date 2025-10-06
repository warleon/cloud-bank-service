#!/usr/bin/env python3
"""
Script principal para ejecutar la ingesta de datos desde las 3 bases de datos en EC2
"""

import os
import sys
import logging
from ingester import DataIngester

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración
S3_BUCKET = os.getenv('S3_BUCKET_NAME', 'cloud-bank-datalake-bucket')


def ingest_postgresql_data():
    """Ingesta datos de PostgreSQL (MS1 - Clientes)"""
    logger.info("="*60)
    logger.info("Iniciando ingesta desde PostgreSQL (MS1 - Clientes)")
    logger.info("="*60)
    
    # Configurar variables de entorno para PostgreSQL
    os.environ['DB_HOST'] = os.getenv('POSTGRES_HOST')
    os.environ['DB_PORT'] = os.getenv('POSTGRES_PORT')
    os.environ['DB_USER'] = os.getenv('POSTGRES_USER')
    os.environ['DB_PASSWORD'] = os.getenv('POSTGRES_PASSWORD')
    os.environ['DB_NAME'] = os.getenv('POSTGRES_DB')
    
    try:
        ingester = DataIngester('postgresql', S3_BUCKET)
        ingester.connect_database()
        
        # Tabla: clientes
        logger.info("Extrayendo tabla 'clientes'...")
        clientes = ingester.extract_data('clientes')
        ingester.upload_to_s3(clientes, 'ms1_clientes')
        logger.info(f"✅ Subidos {len(clientes)} registros de clientes a S3")
        
        # Tabla: documentos_identidad
        logger.info("Extrayendo tabla 'documentos_identidad'...")
        documentos = ingester.extract_data('documentos_identidad')
        ingester.upload_to_s3(documentos, 'ms1_documentos_identidad')
        logger.info(f"✅ Subidos {len(documentos)} registros de documentos a S3")
        
        ingester.close()
        logger.info("✅ Ingesta de PostgreSQL completada\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en ingesta de PostgreSQL: {e}")
        return False


def ingest_mysql_data():
    """Ingesta datos de MySQL (MS2 - Cuentas)"""
    logger.info("="*60)
    logger.info("Iniciando ingesta desde MySQL (MS2 - Cuentas)")
    logger.info("="*60)
    
    # Configurar variables de entorno para MySQL
    os.environ['DB_HOST'] = os.getenv('MYSQL_HOST')
    os.environ['DB_PORT'] = os.getenv('MYSQL_PORT')
    os.environ['DB_USER'] = os.getenv('MYSQL_USER')
    os.environ['DB_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    os.environ['DB_NAME'] = os.getenv('MYSQL_DB')
    
    try:
        ingester = DataIngester('mysql', S3_BUCKET)
        ingester.connect_database()
        
        # Tabla: tipos_cuenta
        logger.info("Extrayendo tabla 'tipos_cuenta'...")
        tipos = ingester.extract_data('tipos_cuenta')
        ingester.upload_to_s3(tipos, 'ms2_tipos_cuenta')
        logger.info(f"✅ Subidos {len(tipos)} registros de tipos de cuenta a S3")
        
        # Tabla: cuentas
        logger.info("Extrayendo tabla 'cuentas'...")
        cuentas = ingester.extract_data('cuentas')
        ingester.upload_to_s3(cuentas, 'ms2_cuentas')
        logger.info(f"✅ Subidos {len(cuentas)} registros de cuentas a S3")
        
        ingester.close()
        logger.info("✅ Ingesta de MySQL completada\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en ingesta de MySQL: {e}")
        return False


def ingest_mongodb_data():
    """Ingesta datos de MongoDB (MS4 - Transacciones)"""
    logger.info("="*60)
    logger.info("Iniciando ingesta desde MongoDB (MS4 - Transacciones)")
    logger.info("="*60)
    
    # Configurar variables de entorno para MongoDB
    os.environ['DB_HOST'] = os.getenv('MONGO_HOST')
    os.environ['DB_PORT'] = os.getenv('MONGO_PORT')
    os.environ['DB_USER'] = os.getenv('MONGO_USER')
    os.environ['DB_PASSWORD'] = os.getenv('MONGO_PASSWORD')
    os.environ['DB_NAME'] = os.getenv('MONGO_DB')
    
    try:
        ingester = DataIngester('mongodb', S3_BUCKET)
        ingester.connect_database()
        
        # Colección: transacciones
        logger.info("Extrayendo colección 'transacciones'...")
        transacciones = ingester.extract_data('transacciones')
        ingester.upload_to_s3(transacciones, 'ms4_transacciones')
        logger.info(f"✅ Subidos {len(transacciones)} documentos de transacciones a S3")
        
        ingester.close()
        logger.info("✅ Ingesta de MongoDB completada\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en ingesta de MongoDB: {e}")
        return False


def main():
    """Función principal"""
    logger.info("🚀 Iniciando proceso de ingesta completo")
    logger.info(f"Bucket S3: {S3_BUCKET}")
    logger.info("")
    
    results = {
        'PostgreSQL': ingest_postgresql_data(),
        'MySQL': ingest_mysql_data(),
        'MongoDB': ingest_mongodb_data()
    }
    
    # Resumen
    logger.info("="*60)
    logger.info("RESUMEN DE INGESTA")
    logger.info("="*60)
    for db, success in results.items():
        status = "✅ EXITOSO" if success else "❌ FALLIDO"
        logger.info(f"{db}: {status}")
    
    logger.info("="*60)
    
    # Exit code
    if all(results.values()):
        logger.info("🎉 Todas las ingestas completadas exitosamente")
        sys.exit(0)
    else:
        logger.error("⚠️  Algunas ingestas fallaron")
        sys.exit(1)


if __name__ == "__main__":
    main()
