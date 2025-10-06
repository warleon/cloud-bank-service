import axios from 'axios';

// IMPORTANTE: Reemplaza estas URLs con las IPs de tus instancias EC2
export const API_ENDPOINTS = {
  clientes: process.env.REACT_APP_MS1_URL || 'http://localhost:8001',
  cuentas: process.env.REACT_APP_MS2_URL || 'http://localhost:8002',
  transacciones: process.env.REACT_APP_MS4_URL || 'http://localhost:8004',
  analytics: process.env.REACT_APP_MS5_URL || 'http://localhost:8000',
  perfilCliente: process.env.REACT_APP_MS3_URL || 'http://localhost:6000'
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

// Cliente Axios para MS5 - Analytics (Athena)
export const analyticsAPI = axios.create({
  baseURL: API_ENDPOINTS.analytics,
  timeout: 30000, // Mayor timeout para queries de Athena
  headers: {
    'Content-Type': 'application/json'
  }
});

// Cliente Axios para MS3 - Perfil Cliente (Vista 360°)
export const perfilClienteAPI = axios.create({
  baseURL: API_ENDPOINTS.perfilCliente,
  timeout: 30000, // Mayor timeout porque agrega datos de múltiples MS
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

// ========== ANALYTICS (MS5 - Athena) ==========
// Dashboard
export const getDashboardEjecutivo = () => analyticsAPI.get('/api/dashboard');

// Clientes Analytics
export const getClientesResumen = () => analyticsAPI.get('/api/clientes/resumen');
export const getClientesLista = (limit = 50) => analyticsAPI.get(`/api/clientes/lista?limit=${limit}`);
export const getClientesConCuentas = (limit = 50) => analyticsAPI.get(`/api/clientes/con-cuentas?limit=${limit}`);

// Cuentas Analytics
export const getCuentasResumen = () => analyticsAPI.get('/api/cuentas/resumen');
export const getCuentasPorTipo = () => analyticsAPI.get('/api/cuentas/por-tipo');
export const getCuentasTopSaldos = (limit = 20) => analyticsAPI.get(`/api/cuentas/top-saldos?limit=${limit}`);

// Transacciones Analytics
export const getTransaccionesResumen = () => analyticsAPI.get('/api/transacciones/resumen');
export const getTransaccionesPorTipo = () => analyticsAPI.get('/api/transacciones/por-tipo');
export const getTransaccionesPorEstado = () => analyticsAPI.get('/api/transacciones/por-estado');
export const getTransaccionesRecientes = (limit = 50) => analyticsAPI.get(`/api/transacciones/recientes?limit=${limit}`);
export const getTransaccionesDetalladas = (limit = 50) => analyticsAPI.get(`/api/transacciones/detalladas?limit=${limit}`);

// Análisis Avanzado
export const getClientesVIP = (threshold = 10000, limit = 20) => 
  analyticsAPI.get(`/api/analisis/clientes-vip?threshold=${threshold}&limit=${limit}`);
export const getActividadDiaria = () => analyticsAPI.get('/api/analisis/actividad-diaria');

// ========== MS3 - PERFIL COMPLETO CLIENTE (Vista 360°) ==========
export const getPerfilCompleto = (clienteId) => perfilClienteAPI.get(`/api/clientes/${clienteId}/perfil-completo`);
export const buscarClientes = (query) => perfilClienteAPI.get(`/api/clientes/buscar?q=${encodeURIComponent(query)}`);
export const getTransaccionesCliente = (clienteId, limit = 50) => 
  perfilClienteAPI.get(`/api/clientes/${clienteId}/transacciones?limit=${limit}`);

