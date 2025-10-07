const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8002;

// Configuración de Swagger
const swaggerOptions = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'MS2 - API de Cuentas Bancarias',
            version: '1.0.0',
            description: 'Microservicio para gestión de cuentas bancarias con MySQL',
            contact: {
                name: 'Cloud Bank Team'
            }
        },
        servers: [
            {
                url: `http://localhost:${PORT}`,
                description: 'Servidor local'
            }
        ],
        tags: [
            {
                name: 'Health',
                description: 'Endpoints de salud del servicio'
            },
            {
                name: 'Cuentas',
                description: 'Operaciones de cuentas bancarias'
            },
            {
                name: 'Tipos de Cuenta',
                description: 'Gestión de tipos de cuenta'
            }
        ]
    },
    apis: ['./server.js']
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);

// Middleware
app.use(cors());
app.use(express.json());

// Swagger UI
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
    customCss: '.swagger-ui .topbar { display: none }',
    customSiteTitle: 'MS2 - API Cuentas'
}));

// Configuración de conexión a MySQL
const dbConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || 'admin',
    password: process.env.DB_PASSWORD || 'admin123',
    database: process.env.DB_NAME || 'cuentas_db',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};

// Pool de conexiones
let pool;

async function initDB(retries = 5, delay = 5000) {
    for (let i = 0; i < retries; i++) {
        try {
            pool = mysql.createPool(dbConfig);
            const connection = await pool.getConnection();
            console.log('✅ Conectado a MySQL');
            connection.release();
            return; // Conexión exitosa
        } catch (error) {
            console.log(`⚠️  Intento ${i + 1}/${retries} - MySQL no disponible aún. Reintentando en ${delay/1000}s...`);
            if (i === retries - 1) {
                console.error('❌ Error al conectar a MySQL después de varios intentos:', error);
                process.exit(1);
            }
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// ============ ENDPOINTS ============

/**
 * @swagger
 * /:
 *   get:
 *     summary: Información del servicio
 *     tags: [Health]
 *     responses:
 *       200:
 *         description: Información básica del microservicio
 */
app.get('/', (req, res) => {
    res.json({
        servicio: 'MS2 - Gestión de Cuentas',
        version: '1.0.0',
        estado: 'activo'
    });
});

/**
 * @swagger
 * /health:
 *   get:
 *     summary: Health check del servicio
 *     tags: [Health]
 *     responses:
 *       200:
 *         description: Servicio saludable
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: healthy
 *                 database:
 *                   type: string
 *                   example: connected
 *       503:
 *         description: Servicio no disponible
 */
app.get('/health', async (req, res) => {
    try {
        await pool.query('SELECT 1');
        res.json({ status: 'healthy', database: 'connected' });
    } catch (error) {
        res.status(503).json({ status: 'unhealthy', database: 'disconnected' });
    }
});

// ===== TIPOS DE CUENTA =====

/**
 * @swagger
 * /tipos-cuenta:
 *   get:
 *     summary: Listar tipos de cuenta bancaria
 *     tags: [Tipos de Cuenta]
 *     responses:
 *       200:
 *         description: Lista de tipos de cuenta activos
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   tipo_cuenta_id:
 *                     type: integer
 *                   nombre:
 *                     type: string
 *                   descripcion:
 *                     type: string
 *                   estado:
 *                     type: string
 */
app.get('/tipos-cuenta', async (req, res) => {
    try {
        const [rows] = await pool.query(
            'SELECT * FROM tipos_cuenta WHERE estado = ?',
            ['activo']
        );
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Obtener tipo de cuenta por ID
app.get('/tipos-cuenta/:id', async (req, res) => {
    try {
        const [rows] = await pool.query(
            'SELECT * FROM tipos_cuenta WHERE tipo_cuenta_id = ?',
            [req.params.id]
        );
        if (rows.length === 0) {
            return res.status(404).json({ error: 'Tipo de cuenta no encontrado' });
        }
        res.json(rows[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ===== CUENTAS =====

/**
 * @swagger
 * /cuentas:
 *   get:
 *     summary: Listar todas las cuentas bancarias
 *     tags: [Cuentas]
 *     responses:
 *       200:
 *         description: Lista de cuentas bancarias
 *   post:
 *     summary: Crear nueva cuenta bancaria
 *     tags: [Cuentas]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - cliente_id
 *               - tipo_cuenta_id
 *             properties:
 *               cliente_id:
 *                 type: integer
 *               tipo_cuenta_id:
 *                 type: integer
 *               saldo:
 *                 type: number
 *                 default: 0
 *               moneda:
 *                 type: string
 *                 default: PEN
 *     responses:
 *       201:
 *         description: Cuenta creada exitosamente
 *       400:
 *         description: Error de validación
 */

// Crear cuenta
app.post('/cuentas', async (req, res) => {
    const { cliente_id, tipo_cuenta_id, saldo, moneda } = req.body;
    
    if (!cliente_id || !tipo_cuenta_id) {
        return res.status(400).json({ error: 'cliente_id y tipo_cuenta_id son requeridos' });
    }

    try {
        // Verificar que el tipo de cuenta existe
        const [tipoRows] = await pool.query(
            'SELECT * FROM tipos_cuenta WHERE tipo_cuenta_id = ? AND estado = ?',
            [tipo_cuenta_id, 'activo']
        );
        
        if (tipoRows.length === 0) {
            return res.status(404).json({ error: 'Tipo de cuenta no encontrado o inactivo' });
        }

        // Generar número de cuenta único
        const numero_cuenta = '100' + Date.now().toString().slice(-10);

        // Insertar cuenta
        const [result] = await pool.query(
            `INSERT INTO cuentas (cliente_id, tipo_cuenta_id, numero_cuenta, saldo, moneda, estado)
             VALUES (?, ?, ?, ?, ?, ?)`,
            [cliente_id, tipo_cuenta_id, numero_cuenta, saldo || 0, moneda || 'PEN', 'activa']
        );

        // Obtener cuenta creada
        const [nuevaCuenta] = await pool.query(
            `SELECT c.*, t.nombre as tipo_cuenta_nombre, t.descripcion as tipo_cuenta_descripcion
             FROM cuentas c
             JOIN tipos_cuenta t ON c.tipo_cuenta_id = t.tipo_cuenta_id
             WHERE c.cuenta_id = ?`,
            [result.insertId]
        );

        res.status(201).json(nuevaCuenta[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Listar todas las cuentas
app.get('/cuentas', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT c.*, t.nombre as tipo_cuenta_nombre, t.descripcion as tipo_cuenta_descripcion
             FROM cuentas c
             JOIN tipos_cuenta t ON c.tipo_cuenta_id = t.tipo_cuenta_id
             ORDER BY c.fecha_apertura DESC`
        );
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Obtener cuenta por ID
app.get('/cuentas/:id', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT c.*, t.nombre as tipo_cuenta_nombre, t.descripcion as tipo_cuenta_descripcion,
                    t.costo_mantenimiento, t.tasa_interes
             FROM cuentas c
             JOIN tipos_cuenta t ON c.tipo_cuenta_id = t.tipo_cuenta_id
             WHERE c.cuenta_id = ?`,
            [req.params.id]
        );
        
        if (rows.length === 0) {
            return res.status(404).json({ error: 'Cuenta no encontrada' });
        }
        
        res.json(rows[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Obtener cuentas por cliente
app.get('/cuentas/cliente/:cliente_id', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT c.*, t.nombre as tipo_cuenta_nombre, t.descripcion as tipo_cuenta_descripcion
             FROM cuentas c
             JOIN tipos_cuenta t ON c.tipo_cuenta_id = t.tipo_cuenta_id
             WHERE c.cliente_id = ?
             ORDER BY c.fecha_apertura DESC`,
            [req.params.cliente_id]
        );
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Obtener cuenta por número de cuenta
app.get('/cuentas/numero/:numero_cuenta', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT c.*, t.nombre as tipo_cuenta_nombre, t.descripcion as tipo_cuenta_descripcion
             FROM cuentas c
             JOIN tipos_cuenta t ON c.tipo_cuenta_id = t.tipo_cuenta_id
             WHERE c.numero_cuenta = ?`,
            [req.params.numero_cuenta]
        );
        
        if (rows.length === 0) {
            return res.status(404).json({ error: 'Cuenta no encontrada' });
        }
        
        res.json(rows[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Actualizar saldo de cuenta
app.patch('/cuentas/:id/saldo', async (req, res) => {
    const { monto, operacion } = req.body; // operacion: 'deposito' o 'retiro'
    
    if (!monto || !operacion) {
        return res.status(400).json({ error: 'monto y operacion son requeridos' });
    }

    if (!['deposito', 'retiro'].includes(operacion)) {
        return res.status(400).json({ error: 'operacion debe ser "deposito" o "retiro"' });
    }

    const connection = await pool.getConnection();
    
    try {
        await connection.beginTransaction();

        // Obtener cuenta actual
        const [cuentas] = await connection.query(
            'SELECT * FROM cuentas WHERE cuenta_id = ? AND estado = ?',
            [req.params.id, 'activa']
        );

        if (cuentas.length === 0) {
            await connection.rollback();
            return res.status(404).json({ error: 'Cuenta no encontrada o no activa' });
        }

        const cuenta = cuentas[0];
        let nuevoSaldo;

        if (operacion === 'deposito') {
            nuevoSaldo = parseFloat(cuenta.saldo) + parseFloat(monto);
        } else {
            nuevoSaldo = parseFloat(cuenta.saldo) - parseFloat(monto);
            if (nuevoSaldo < 0) {
                await connection.rollback();
                return res.status(400).json({ error: 'Saldo insuficiente' });
            }
        }

        // Actualizar saldo
        await connection.query(
            'UPDATE cuentas SET saldo = ? WHERE cuenta_id = ?',
            [nuevoSaldo, req.params.id]
        );

        await connection.commit();

        // Obtener cuenta actualizada
        const [cuentaActualizada] = await pool.query(
            `SELECT c.*, t.nombre as tipo_cuenta_nombre
             FROM cuentas c
             JOIN tipos_cuenta t ON c.tipo_cuenta_id = t.tipo_cuenta_id
             WHERE c.cuenta_id = ?`,
            [req.params.id]
        );

        res.json(cuentaActualizada[0]);
    } catch (error) {
        await connection.rollback();
        res.status(500).json({ error: error.message });
    } finally {
        connection.release();
    }
});

// Actualizar estado de cuenta
app.patch('/cuentas/:id/estado', async (req, res) => {
    const { estado } = req.body;
    
    if (!estado || !['activa', 'bloqueada', 'cerrada'].includes(estado)) {
        return res.status(400).json({ error: 'Estado inválido. Use: activa, bloqueada, cerrada' });
    }

    try {
        await pool.query(
            'UPDATE cuentas SET estado = ? WHERE cuenta_id = ?',
            [estado, req.params.id]
        );

        const [cuenta] = await pool.query(
            'SELECT * FROM cuentas WHERE cuenta_id = ?',
            [req.params.id]
        );

        if (cuenta.length === 0) {
            return res.status(404).json({ error: 'Cuenta no encontrada' });
        }

        res.json(cuenta[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Eliminar cuenta
app.delete('/cuentas/:id', async (req, res) => {
    try {
        const [cuenta] = await pool.query(
            'SELECT * FROM cuentas WHERE cuenta_id = ?',
            [req.params.id]
        );

        if (cuenta.length === 0) {
            return res.status(404).json({ error: 'Cuenta no encontrada' });
        }

        if (cuenta[0].saldo > 0) {
            return res.status(400).json({ error: 'No se puede eliminar una cuenta con saldo' });
        }

        await pool.query('DELETE FROM cuentas WHERE cuenta_id = ?', [req.params.id]);
        res.json({ mensaje: 'Cuenta eliminada exitosamente' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Iniciar servidor
initDB().then(() => {
    app.listen(PORT, '0.0.0.0', () => {
        console.log(`🚀 MS2 - Gestión de Cuentas corriendo en puerto ${PORT}`);
    });
});
