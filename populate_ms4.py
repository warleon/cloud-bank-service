#!/usr/bin/env python3
"""
Script para poblar MongoDB (MS4) con 20,000 transacciones
"""
from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta
from bson import ObjectId
import sys

fake = Faker('es_ES')

# Configuración de MongoDB
DB_CONFIG = {
    'host': 'localhost',  # Ejecutar desde el mismo EC2 de MS4
    'port': 27017,
    'username': 'admin',
    'password': 'admin123',
    'database': 'transacciones_db'
}

def create_connection():
    """Crear conexión a MongoDB"""
    try:
        connection_string = f"mongodb://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?authSource=admin"
        client = MongoClient(connection_string)
        db = client[DB_CONFIG['database']]
        # Test connection
        db.command('ping')
        print("✅ Conectado a MongoDB (MS4)")
        return client, db
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        sys.exit(1)

def clear_collection(db):
    """Limpiar colección de transacciones"""
    try:
        db.transacciones.delete_many({})
        print("🧹 Colección transacciones limpiada")
    except Exception as e:
        print(f"⚠️  Error limpiando colección: {e}")

def insert_transacciones_batch(db, num_records=20000, batch_size=1000):
    """Insertar transacciones en lotes"""
    total_inserted = 0
    
    tipos_transaccion = ['deposito', 'retiro', 'transferencia', 'pago_servicio']
    estados = ['completada', 'completada', 'completada', 'pendiente', 'fallida']  # 60% completadas
    
    print(f"📝 Insertando {num_records} transacciones en lotes de {batch_size}...")
    
    for batch_start in range(0, num_records, batch_size):
        transacciones_batch = []
        
        for i in range(batch_start, min(batch_start + batch_size, num_records)):
            transaccion_id = str(i + 1)
            
            tipo = random.choice(tipos_transaccion)
            monto = round(random.uniform(10, 10000), 2)
            fecha = datetime.now() - timedelta(days=random.randint(0, 365))
            estado = random.choice(estados)
            
            # Asignar cuentas (del 1 al 20000)
            cuenta_origen_id = random.randint(1, 20000)
            
            if tipo == 'transferencia':
                # Transferencia entre cuentas diferentes
                cuenta_destino_id = random.randint(1, 20000)
                while cuenta_destino_id == cuenta_origen_id:
                    cuenta_destino_id = random.randint(1, 20000)
                descripcion = f"Transferencia a cuenta {cuenta_destino_id}"
            elif tipo == 'deposito':
                cuenta_destino_id = cuenta_origen_id
                descripcion = f"Depósito en cuenta {cuenta_origen_id}"
            elif tipo == 'retiro':
                cuenta_destino_id = None
                descripcion = f"Retiro de efectivo"
            else:  # pago_servicio
                cuenta_destino_id = None
                descripcion = f"Pago de {random.choice(['luz', 'agua', 'internet', 'teléfono', 'Netflix', 'Spotify'])}"
            
            transaccion = {
                'transaccionId': transaccion_id,
                'tipo': tipo,
                'monto': monto,
                'fecha': fecha,
                'estado': estado,
                'descripcion': descripcion,
                'cuentaOrigenId': cuenta_origen_id,
                'cuentaDestinoId': cuenta_destino_id,
                'metadata': {
                    'ip': fake.ipv4(),
                    'dispositivo': random.choice(['web', 'mobile', 'atm']),
                    'ubicacion': fake.city()
                }
            }
            
            transacciones_batch.append(transaccion)
        
        # Insertar lote
        try:
            db.transacciones.insert_many(transacciones_batch)
            total_inserted += len(transacciones_batch)
            print(f"   ✅ Insertadas {total_inserted}/{num_records} transacciones...")
            
        except Exception as e:
            print(f"   ❌ Error insertando lote: {e}")
            break
    
    return total_inserted

def main():
    print("=" * 60)
    print("🚀 POBLANDO MS4 (MongoDB) CON 20,000 TRANSACCIONES")
    print("=" * 60)
    
    client, db = create_connection()
    
    # Limpiar colección existente
    clear_collection(db)
    
    # Insertar 20,000 transacciones
    total = insert_transacciones_batch(db, num_records=20000, batch_size=1000)
    
    # Verificar
    count = db.transacciones.count_documents({})
    
    print("=" * 60)
    print(f"✅ COMPLETADO: {count} transacciones insertadas en MongoDB")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    main()
