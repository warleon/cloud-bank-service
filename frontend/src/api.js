import axios from 'axios';

// IMPORTANTE: Reemplaza estas URLs con las IPs de tus instancias EC2
export const API_ENDPOINTS = {
  clientes: process.env.REACT_APP_MS1_URL || 'http://localhost:8001',
  cuentas: process.env.REACT_APP_MS2_URL || 'http://localhost:8002',
  transacciones: process.env.REACT_APP_MS4_URL || 'http://localhost:8004'
};

// Cliente Axios para MS1 - Clientes
export const clientesAPI = axios.create({
  baseURL: API_ENDPOINTS.clientes,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Cliente Axios para MS2 - Cuentas
export const cuentasAPI = axios.create({
  baseURL: API_ENDPOINTS.cuentas,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Cliente Axios para MS4 - Transacciones
export const transaccionesAPI = axios.create({
  baseURL: API_ENDPOINTS.transacciones,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Funciones de la API

// ========== CLIENTES ==========
export const getClientes = () => clientesAPI.get('/clientes');
export const getCliente = (id) => clientesAPI.get(`/clientes/${id}`);
export const crearCliente = (data) => clientesAPI.post('/clientes', data);
export const actualizarCliente = (id, data) => clientesAPI.put(`/clientes/${id}`, data);
export const eliminarCliente = (id) => clientesAPI.delete(`/clientes/${id}`);

// ========== CUENTAS ==========
export const getCuentas = () => cuentasAPI.get('/cuentas');
export const getCuenta = (id) => cuentasAPI.get(`/cuentas/${id}`);
export const getCuentasPorCliente = (clienteId) => cuentasAPI.get(`/cuentas/cliente/${clienteId}`);
export const getTiposCuenta = () => cuentasAPI.get('/tipos-cuenta');
export const crearCuenta = (data) => cuentasAPI.post('/cuentas', data);
export const actualizarSaldo = (id, data) => cuentasAPI.patch(`/cuentas/${id}/saldo`, data);

// ========== TRANSACCIONES ==========
export const getTransacciones = () => transaccionesAPI.get('/transacciones');
export const getTransaccion = (id) => transaccionesAPI.get(`/transacciones/${id}`);
export const getTransaccionesPorCuenta = (cuentaId) => transaccionesAPI.get(`/transacciones/cuenta/${cuentaId}`);
export const crearTransaccion = (data) => transaccionesAPI.post('/transacciones', data);
export const actualizarEstadoTransaccion = (id, estado) => transaccionesAPI.patch(`/transacciones/${id}/estado`, { estado });
