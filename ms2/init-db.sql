-- Tabla de Tipos de Cuenta
CREATE TABLE IF NOT EXISTS tipos_cuenta (
    tipo_cuenta_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    costo_mantenimiento DECIMAL(10, 2) DEFAULT 0.00,
    tasa_interes DECIMAL(5, 2) DEFAULT 0.00,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Cuentas (relación con tipos_cuenta y cliente_id externo)
CREATE TABLE IF NOT EXISTS cuentas (
    cuenta_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo_cuenta_id INT NOT NULL,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    saldo DECIMAL(15, 2) DEFAULT 0.00,
    moneda VARCHAR(3) DEFAULT 'PEN' CHECK (moneda IN ('PEN', 'USD', 'EUR')),
    fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activa' CHECK (estado IN ('activa', 'bloqueada', 'cerrada')),
    FOREIGN KEY (tipo_cuenta_id) REFERENCES tipos_cuenta(tipo_cuenta_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Índices para mejorar rendimiento
CREATE INDEX idx_cuentas_cliente ON cuentas(cliente_id);
CREATE INDEX idx_cuentas_numero ON cuentas(numero_cuenta);
CREATE INDEX idx_cuentas_estado ON cuentas(estado);

-- Datos de ejemplo - Tipos de Cuenta
INSERT INTO tipos_cuenta (nombre, descripcion, costo_mantenimiento, tasa_interes, estado) VALUES
('Cuenta Sueldo', 'Cuenta sin costo de mantenimiento para depósito de sueldo', 0.00, 0.00, 'activo'),
('Cuenta Free', 'Cuenta gratuita con servicios básicos', 0.00, 0.50, 'activo'),
('Cuenta Premium', 'Cuenta con beneficios adicionales', 15.00, 1.50, 'activo'),
('Cuenta Ahorro', 'Cuenta de ahorros con mayor tasa de interés', 5.00, 3.00, 'activo');

-- Datos de ejemplo - Cuentas (cliente_id debe corresponder a MS1)
INSERT INTO cuentas (cliente_id, tipo_cuenta_id, numero_cuenta, saldo, moneda, estado) VALUES
(1, 1, '1001234567890', 5000.00, 'PEN', 'activa'),
(1, 4, '1001234567891', 10000.00, 'USD', 'activa'),
(2, 2, '1002345678901', 3500.50, 'PEN', 'activa'),
(3, 3, '1003456789012', 15000.00, 'PEN', 'activa');
