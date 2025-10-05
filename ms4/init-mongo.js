// Crear base de datos y colección
db = db.getSiblingDB('transacciones_db');

// Crear colección de transacciones
db.createCollection('transacciones');

// Crear índices
db.transacciones.createIndex({ "transaccionId": 1 }, { unique: true });
db.transacciones.createIndex({ "cuentaOrigenId": 1 });
db.transacciones.createIndex({ "cuentaDestinoId": 1 });
db.transacciones.createIndex({ "fecha": -1 });
db.transacciones.createIndex({ "tipo": 1 });
db.transacciones.createIndex({ "estado": 1 });

// Insertar datos de ejemplo
db.transacciones.insertMany([
    {
        transaccionId: "TRX001",
        tipo: "DEPOSITO",
        cuentaOrigenId: null,
        cuentaDestinoId: 1,
        monto: 1000.00,
        moneda: "PEN",
        descripcion: "Depósito inicial",
        fecha: new Date("2024-01-15T10:30:00Z"),
        estado: "COMPLETADA",
        metadata: {
            canal: "CAJERO",
            ubicacion: "Lima, Perú"
        }
    },
    {
        transaccionId: "TRX002",
        tipo: "RETIRO",
        cuentaOrigenId: 1,
        cuentaDestinoId: null,
        monto: 200.00,
        moneda: "PEN",
        descripcion: "Retiro cajero automático",
        fecha: new Date("2024-01-16T14:45:00Z"),
        estado: "COMPLETADA",
        metadata: {
            canal: "CAJERO",
            ubicacion: "Lima, Perú"
        }
    },
    {
        transaccionId: "TRX003",
        tipo: "TRANSFERENCIA",
        cuentaOrigenId: 1,
        cuentaDestinoId: 2,
        monto: 500.00,
        moneda: "PEN",
        descripcion: "Transferencia entre cuentas",
        fecha: new Date("2024-01-17T09:15:00Z"),
        estado: "COMPLETADA",
        metadata: {
            canal: "WEB",
            ip: "192.168.1.100"
        }
    },
    {
        transaccionId: "TRX004",
        tipo: "PAGO_SERVICIO",
        cuentaOrigenId: 2,
        cuentaDestinoId: null,
        monto: 150.50,
        moneda: "PEN",
        descripcion: "Pago de luz",
        fecha: new Date("2024-01-18T16:20:00Z"),
        estado: "COMPLETADA",
        metadata: {
            canal: "MOVIL",
            servicio: "LUZ_DEL_SUR"
        }
    },
    {
        transaccionId: "TRX005",
        tipo: "TRANSFERENCIA",
        cuentaOrigenId: 3,
        cuentaDestinoId: 1,
        monto: 750.00,
        moneda: "PEN",
        descripcion: "Pago de servicio",
        fecha: new Date("2024-01-19T11:00:00Z"),
        estado: "PENDIENTE",
        metadata: {
            canal: "WEB"
        }
    }
]);

print("✅ Base de datos y colecciones creadas con datos de ejemplo");
