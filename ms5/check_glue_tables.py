"""
Script para verificar las tablas en Glue Catalog
"""
import boto3
import json

def list_glue_tables():
    glue = boto3.client('glue', region_name='us-east-1')
    
    try:
        response = glue.get_tables(DatabaseName='cloud_bank_db')
        
        print("=" * 60)
        print("TABLAS EN GLUE CATALOG - cloud_bank_db")
        print("=" * 60)
        
        if not response['TableList']:
            print("❌ No se encontraron tablas en la base de datos")
            return
        
        for table in response['TableList']:
            print(f"\n📊 Tabla: {table['Name']}")
            print(f"   Location: {table['StorageDescriptor']['Location']}")
            print(f"   Columnas:")
            for col in table['StorageDescriptor']['Columns']:
                print(f"      - {col['Name']}: {col['Type']}")
        
        print("\n" + "=" * 60)
        print(f"Total de tablas: {len(response['TableList'])}")
        print("=" * 60)
        
        # Guardar en archivo JSON
        with open('glue_tables.json', 'w') as f:
            json.dump(response['TableList'], f, indent=2, default=str)
        print("\n✅ Información guardada en glue_tables.json")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    list_glue_tables()
