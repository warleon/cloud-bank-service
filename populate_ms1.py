#!/usr/bin/env python3
"""
Script para poblar PostgreSQL (MS1) con 20,000 clientes
"""
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import sys

fake = Faker('es_ES')

# Configuración de PostgreSQL
DB_CONFIG = {
    'host': 'localhost',  # Ejecutar desde el mismo EC2 de MS1
    'port': 5432,
    'database': 'clientes_db',
    'user': 'admin',
    'password': 'admin123'
}

def create_connection():
    """Crear conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conectado a PostgreSQL (MS1)")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        sys.exit(1)

def clear_tables(conn):
    """Limpiar tablas existentes"""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM documentos_identidad;")
        cursor.execute("DELETE FROM clientes;")
        conn.commit()
        print("🧹 Tablas limpiadas")
    except Exception as e:
        conn.rollback()
        print(f"⚠️  Error limpiando tablas: {e}")
    finally:
        cursor.close()

def insert_clientes_batch(conn, num_records=20000, batch_size=1000):
    """Insertar clientes en lotes"""
    cursor = conn.cursor()
    total_inserted = 0
    
    print(f"📝 Insertando {num_records} clientes en lotes de {batch_size}...")
    
    for batch_start in range(0, num_records, batch_size):
        clientes_batch = []
        documentos_batch = []
        
        for i in range(batch_start, min(batch_start + batch_size, num_records)):
            cliente_id = i + 1
            
            # Datos del cliente
            nombre = fake.first_name()
            apellido = fake.last_name()
            email = f"{nombre.lower()}.{apellido.lower()}{cliente_id}@{fake.free_email_domain()}"
            telefono = fake.phone_number()[:15]
            direccion = fake.address().replace('\n', ', ')[:200]
            fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=80)
            estado = random.choice(['activo', 'activo', 'activo', 'inactivo'])  # 75% activos
            fecha_registro = datetime.now() - timedelta(days=random.randint(0, 365*5))
            
            clientes_batch.append((
                cliente_id, nombre, apellido, email, telefono, direccion,
                fecha_nacimiento, estado, fecha_registro
            ))
            
            # Documento de identidad
            tipo_doc = random.choice(['DNI', 'DNI', 'DNI', 'Pasaporte', 'CE'])  # Mayoría DNI
            if tipo_doc == 'DNI':
                numero_doc = str(random.randint(10000000, 99999999))
            elif tipo_doc == 'Pasaporte':
                numero_doc = fake.passport_number()
            else:
                numero_doc = str(random.randint(100000000, 999999999))
            
            fecha_emision = fecha_registro.date()
            fecha_vencimiento = fecha_emision + timedelta(days=random.randint(365*3, 365*10))
            
            documentos_batch.append((
                cliente_id, tipo_doc, numero_doc, fecha_emision, fecha_vencimiento
            ))
        
        # Insertar lote de clientes
        try:
            cursor.executemany("""
                INSERT INTO clientes 
                (cliente_id, nombre, apellido, email, telefono, direccion, 
                 fecha_nacimiento, estado, fecha_registro)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, clientes_batch)
            
            cursor.executemany("""
                INSERT INTO documentos_identidad 
                (cliente_id, tipo_documento, numero_documento, fecha_emision, fecha_vencimiento)
                VALUES (%s, %s, %s, %s, %s)
            """, documentos_batch)
            
            conn.commit()
            total_inserted += len(clientes_batch)
            print(f"   ✅ Insertados {total_inserted}/{num_records} clientes...")
            
        except Exception as e:
            conn.rollback()
            print(f"   ❌ Error insertando lote: {e}")
            break
    
    cursor.close()
    return total_inserted

def main():
    print("=" * 60)
    print("🚀 POBLANDO MS1 (PostgreSQL) CON 20,000 CLIENTES")
    print("=" * 60)
    
    conn = create_connection()
    
    # Limpiar tablas existentes
    clear_tables(conn)
    
    # Insertar 20,000 clientes
    total = insert_clientes_batch(conn, num_records=20000, batch_size=1000)
    
    # Verificar
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes;")
    count = cursor.fetchone()[0]
    cursor.close()
    
    print("=" * 60)
    print(f"✅ COMPLETADO: {count} clientes insertados en PostgreSQL")
    print("=" * 60)
    
    conn.close()

if __name__ == "__main__":
    main()
