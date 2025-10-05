-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'bloqueado'))
);

-- Tabla de Documentos de Identidad (relación con clientes)
CREATE TABLE IF NOT EXISTS documentos_identidad (
    documento_id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    tipo_documento VARCHAR(20) NOT NULL CHECK (tipo_documento IN ('DNI', 'Pasaporte', 'RUC', 'Carnet Extranjeria')),
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_emision DATE,
    fecha_vencimiento DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_documentos_numero ON documentos_identidad(numero_documento);
CREATE INDEX idx_documentos_cliente ON documentos_identidad(cliente_id);

-- Datos de ejemplo
INSERT INTO clientes (nombre, apellido, email, telefono, estado) VALUES
('Juan', 'Pérez', 'juan.perez@email.com', '999888777', 'activo'),
('María', 'García', 'maria.garcia@email.com', '999777666', 'activo'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '999666555', 'activo');

INSERT INTO documentos_identidad (cliente_id, tipo_documento, numero_documento, fecha_emision, fecha_vencimiento) VALUES
(1, 'DNI', '12345678', '2020-01-15', '2030-01-15'),
(2, 'DNI', '87654321', '2019-05-20', '2029-05-20'),
(3, 'Pasaporte', 'P1234567', '2021-03-10', '2031-03-10');
