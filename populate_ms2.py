#!/usr/bin/env python3
"""
Script para poblar MySQL (MS2) con 20,000 cuentas (una por cliente)
"""
import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal
import sys

fake = Faker('es_ES')

# Configuración de MySQL
DB_CONFIG = {
    'host': 'localhost',  # Ejecutar desde el mismo EC2 de MS2
    'port': 3306,
    'database': 'cuentas_db',
    'user': 'admin',
    'password': 'admin123'
}

def create_connection():
    """Crear conexión a MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conectado a MySQL (MS2)")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        sys.exit(1)

def clear_tables(conn):
    """Limpiar tabla de cuentas"""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cuentas;")
        conn.commit()
        print("🧹 Tabla cuentas limpiada")
    except Exception as e:
        conn.rollback()
        print(f"⚠️  Error limpiando tabla: {e}")
    finally:
        cursor.close()

def get_tipo_cuenta_ids(conn):
    """Obtener IDs de tipos de cuenta disponibles"""
    cursor = conn.cursor()
    cursor.execute("SELECT tipo_cuenta_id FROM tipos_cuenta;")
    tipos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    if not tipos:
        print("⚠️  No hay tipos de cuenta. Insertando tipos por defecto...")
        insert_tipos_cuenta(conn)
        return get_tipo_cuenta_ids(conn)
    return tipos

def insert_tipos_cuenta(conn):
    """Insertar tipos de cuenta por defecto si no existen"""
    cursor = conn.cursor()
    tipos = [
        (1, 'Ahorro', 'Cuenta de ahorros personal'),
        (2, 'Corriente', 'Cuenta corriente empresarial'),
        (3, 'Nómina', 'Cuenta para recepción de salarios'),
        (4, 'Inversión', 'Cuenta de inversión a plazo fijo')
    ]
    try:
        cursor.executemany("""
            INSERT INTO tipos_cuenta (tipo_cuenta_id, nombre, descripcion)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE nombre=VALUES(nombre)
        """, tipos)
        conn.commit()
        print("✅ Tipos de cuenta insertados")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error insertando tipos: {e}")
    finally:
        cursor.close()

def insert_cuentas_batch(conn, num_records=20000, batch_size=1000):
    """Insertar cuentas en lotes (una por cliente)"""
    cursor = conn.cursor()
    total_inserted = 0
    
    tipos_cuenta = get_tipo_cuenta_ids(conn)
    
    print(f"📝 Insertando {num_records} cuentas en lotes de {batch_size}...")
    
    for batch_start in range(0, num_records, batch_size):
        cuentas_batch = []
        
        for i in range(batch_start, min(batch_start + batch_size, num_records)):
            cuenta_id = i + 1
            cliente_id = i + 1  # Una cuenta por cliente
            
            # Generar número de cuenta (16 dígitos)
            numero_cuenta = f"{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
            
            tipo_cuenta_id = random.choice(tipos_cuenta)
            
            # Saldo aleatorio entre 100 y 500,000 PEN
            saldo = round(random.uniform(100, 500000), 2)
            
            moneda = 'PEN'
            fecha_apertura = datetime.now() - timedelta(days=random.randint(0, 365*5))
            estado = random.choice(['activa', 'activa', 'activa', 'bloqueada'])  # 75% activas, 25% bloqueadas
            
            cuentas_batch.append((
                cuenta_id, cliente_id, numero_cuenta, tipo_cuenta_id,
                saldo, moneda, fecha_apertura, estado
            ))
        
        # Insertar lote
        try:
            cursor.executemany("""
                INSERT INTO cuentas 
                (cuenta_id, cliente_id, numero_cuenta, tipo_cuenta_id, 
                 saldo, moneda, fecha_apertura, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, cuentas_batch)
            
            conn.commit()
            total_inserted += len(cuentas_batch)
            print(f"   ✅ Insertadas {total_inserted}/{num_records} cuentas...")
            
        except Exception as e:
            conn.rollback()
            print(f"   ❌ Error insertando lote: {e}")
            break
    
    cursor.close()
    return total_inserted

def main():
    print("=" * 60)
    print("🚀 POBLANDO MS2 (MySQL) CON 20,000 CUENTAS")
    print("=" * 60)
    
    conn = create_connection()
    
    # Limpiar tabla existente
    clear_tables(conn)
    
    # Insertar 20,000 cuentas
    total = insert_cuentas_batch(conn, num_records=20000, batch_size=1000)
    
    # Verificar
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cuentas;")
    count = cursor.fetchone()[0]
    cursor.close()
    
    print("=" * 60)
    print(f"✅ COMPLETADO: {count} cuentas insertadas en MySQL")
    print("=" * 60)
    
    conn.close()

if __name__ == "__main__":
    main()
