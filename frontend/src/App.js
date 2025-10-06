import React, { useState, useEffect } from 'react';
import './App.css';
import {
  getClientes,
  crearCliente,
  getCuentas,
  getCuentasPorCliente,
  getTiposCuenta,
  crearCuenta,
  actualizarSaldo,
  getTransacciones,
  getTransaccionesPorCuenta,
  crearTransaccion,
  getDashboardEjecutivo,
  getCuentasResumen,
  getCuentasPorTipo,
  getCuentasTopSaldos,
  getTransaccionesResumen,
  getTransaccionesPorTipo,
  getTransaccionesDetalladas,
  getClientesVIP
} from './api';

function App() {
  const [vista, setVista] = useState('clientes');
  const [clientes, setClientes] = useState([]);
  const [cuentas, setCuentas] = useState([]);
  const [transacciones, setTransacciones] = useState([]);
  const [tiposCuenta, setTiposCuenta] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState('');

  // Estados para Analytics
  const [dashboardData, setDashboardData] = useState(null);
  const [cuentasAnalytics, setCuentasAnalytics] = useState(null);
  const [transaccionesAnalytics, setTransaccionesAnalytics] = useState(null);
  const [clientesVIP, setClientesVIP] = useState([]);

  // Estados para formularios
  const [nuevoCliente, setNuevoCliente] = useState({
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    documento: {
      tipo_documento: 'DNI',
      numero_documento: '',
      fecha_emision: '',
      fecha_vencimiento: ''
    }
  });

  const [nuevaCuenta, setNuevaCuenta] = useState({
    cliente_id: '',
    tipo_cuenta_id: '',
    saldo: 0,
    moneda: 'PEN'
  });

  const [nuevaTransaccion, setNuevaTransaccion] = useState({
    tipo: 'DEPOSITO',
    cuentaOrigenId: '',
    cuentaDestinoId: '',
    monto: 0,
    moneda: 'PEN',
    descripcion: ''
  });

  // Cargar datos iniciales
  useEffect(() => {
    cargarDatos();
  }, [vista]);

  const cargarDatos = async () => {
    if (vista === 'analytics') {
      cargarAnalytics();
      return;
    }

    setLoading(true);
    try {
      if (vista === 'clientes') {
        const res = await getClientes();
        setClientes(Array.isArray(res.data) ? res.data : []);
      } else if (vista === 'cuentas') {
        const [cuentasRes, tiposRes, clientesRes] = await Promise.all([
          getCuentas(),
          getTiposCuenta(),
          getClientes()
        ]);
        setCuentas(Array.isArray(cuentasRes.data) ? cuentasRes.data : []);
        setTiposCuenta(Array.isArray(tiposRes.data) ? tiposRes.data : []);
        setClientes(Array.isArray(clientesRes.data) ? clientesRes.data : []);
      } else if (vista === 'transacciones') {
        const [transaccionesRes, cuentasRes] = await Promise.all([
          getTransacciones(),
          getCuentas()
        ]);
        setTransacciones(Array.isArray(transaccionesRes.data) ? transaccionesRes.data : []);
        setCuentas(Array.isArray(cuentasRes.data) ? cuentasRes.data : []);
      }
    } catch (error) {
      console.error('Error al cargar datos:', error);
      mostrarMensaje('Error al cargar datos: ' + (error.response?.data?.detail || error.message), 'error');
      // Resetear estados a arrays vacíos
      if (vista === 'clientes') setClientes([]);
      if (vista === 'cuentas') { setCuentas([]); setTiposCuenta([]); }
      if (vista === 'transacciones') { setTransacciones([]); setCuentas([]); }
    } finally {
      setLoading(false);
    }
  };

  const mostrarMensaje = (msg, tipo = 'success') => {
    setMensaje({ texto: msg, tipo });
    setTimeout(() => setMensaje(''), 3000);
  };

  // Handlers para clientes
  const handleCrearCliente = async (e) => {
    e.preventDefault();
    try {
      // Preparar datos: convertir strings vacíos a null para fechas
      const clienteData = {
        ...nuevoCliente,
        documento: {
          ...nuevoCliente.documento,
          fecha_emision: nuevoCliente.documento.fecha_emision || null,
          fecha_vencimiento: nuevoCliente.documento.fecha_vencimiento || null
        }
      };
      await crearCliente(clienteData);
      mostrarMensaje('Cliente creado exitosamente');
      cargarDatos();
      setNuevoCliente({
        nombre: '',
        apellido: '',
        email: '',
        telefono: '',
        documento: {
          tipo_documento: 'DNI',
          numero_documento: '',
          fecha_emision: '',
          fecha_vencimiento: ''
        }
      });
    } catch (error) {
      mostrarMensaje('Error al crear cliente: ' + (error.response?.data?.detail || error.message), 'error');
      console.error('Error completo:', error.response?.data);
    }
  };

  // Handlers para cuentas
  const handleCrearCuenta = async (e) => {
    e.preventDefault();
    try {
      await crearCuenta({
        ...nuevaCuenta,
        cliente_id: parseInt(nuevaCuenta.cliente_id),
        tipo_cuenta_id: parseInt(nuevaCuenta.tipo_cuenta_id)
      });
      mostrarMensaje('Cuenta creada exitosamente');
      cargarDatos();
      setNuevaCuenta({ cliente_id: '', tipo_cuenta_id: '', saldo: 0, moneda: 'PEN' });
    } catch (error) {
      mostrarMensaje('Error al crear cuenta: ' + error.response?.data?.error, 'error');
    }
  };

  // Handlers para transacciones
  const handleCrearTransaccion = async (e) => {
    e.preventDefault();
    try {
      const data = {
        tipo: nuevaTransaccion.tipo,
        monto: parseFloat(nuevaTransaccion.monto),
        moneda: nuevaTransaccion.moneda,
        descripcion: nuevaTransaccion.descripcion || 'Sin descripción'
      };

      if (nuevaTransaccion.tipo === 'DEPOSITO' || nuevaTransaccion.tipo === 'TRANSFERENCIA') {
        data.cuentaDestinoId = parseInt(nuevaTransaccion.cuentaDestinoId);
      }
      
      if (nuevaTransaccion.tipo === 'RETIRO' || nuevaTransaccion.tipo === 'TRANSFERENCIA' || nuevaTransaccion.tipo === 'PAGO_SERVICIO') {
        data.cuentaOrigenId = parseInt(nuevaTransaccion.cuentaOrigenId);
      }

      console.log('Enviando transacción:', data);
      await crearTransaccion(data);
      mostrarMensaje('Transacción creada exitosamente');
      cargarDatos();
      setNuevaTransaccion({
        tipo: 'DEPOSITO',
        cuentaOrigenId: '',
        cuentaDestinoId: '',
        monto: 0,
        moneda: 'PEN',
        descripcion: ''
      });
    } catch (error) {
      console.error('Error completo:', error.response);
      mostrarMensaje('Error al crear transacción: ' + (error.response?.data?.message || error.response?.data?.error || error.message), 'error');
    }
  };

  // Cargar datos de Analytics
  const cargarAnalytics = async () => {
    setLoading(true);
    try {
      const [dashboard, cuentasRes, transRes, vips] = await Promise.all([
        getDashboardEjecutivo(),
        getCuentasPorTipo(),
        getTransaccionesPorTipo(),
        getClientesVIP(10000, 10) // VIPs con patrimonio > 10,000
      ]);
      
      // Transformar array del dashboard a objeto
      const dashboardObj = {};
      if (dashboard.data && dashboard.data.data) {
        dashboard.data.data.forEach(item => {
          const key = item.metrica.toLowerCase().replace(/ /g, '_');
          dashboardObj[key] = item.valor;
        });
        // Agregar moneda por defecto
        dashboardObj.moneda_principal = 'PEN';
      }
      
      setDashboardData(dashboardObj);
      setCuentasAnalytics(cuentasRes.data);
      setTransaccionesAnalytics(transRes.data);
      setClientesVIP(vips.data.results || vips.data.data || []);
    } catch (error) {
      mostrarMensaje('Error al cargar analytics: ' + (error.response?.data?.error || error.message), 'error');
      console.error('Error en analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏦 Cloud Bank</h1>
        <p>Sistema de Gestión Bancaria</p>
      </header>

      {mensaje && (
        <div className={`mensaje ${mensaje.tipo}`}>
          {mensaje.texto}
        </div>
      )}

      <nav className="nav-menu">
        <button 
          className={vista === 'clientes' ? 'active' : ''} 
          onClick={() => setVista('clientes')}
        >
          👤 Clientes
        </button>
        <button 
          className={vista === 'cuentas' ? 'active' : ''} 
          onClick={() => setVista('cuentas')}
        >
          💳 Cuentas
        </button>
        <button 
          className={vista === 'transacciones' ? 'active' : ''} 
          onClick={() => setVista('transacciones')}
        >
          💸 Transacciones
        </button>
        <button 
          className={vista === 'analytics' ? 'active' : ''} 
          onClick={() => setVista('analytics')}
        >
          📊 Analytics
        </button>
      </nav>

      <main className="main-content">
        {loading ? (
          <div className="loading">Cargando...</div>
        ) : (
          <>
            {/* VISTA CLIENTES */}
            {vista === 'clientes' && (
              <div className="vista-container">
                <div className="formulario-section">
                  <h2>Registrar Cliente</h2>
                  <form onSubmit={handleCrearCliente}>
                    <input
                      type="text"
                      placeholder="Nombre"
                      value={nuevoCliente.nombre}
                      onChange={(e) => setNuevoCliente({...nuevoCliente, nombre: e.target.value})}
                      required
                    />
                    <input
                      type="text"
                      placeholder="Apellido"
                      value={nuevoCliente.apellido}
                      onChange={(e) => setNuevoCliente({...nuevoCliente, apellido: e.target.value})}
                      required
                    />
                    <input
                      type="email"
                      placeholder="Email"
                      value={nuevoCliente.email}
                      onChange={(e) => setNuevoCliente({...nuevoCliente, email: e.target.value})}
                      required
                    />
                    <input
                      type="tel"
                      placeholder="Teléfono"
                      value={nuevoCliente.telefono}
                      onChange={(e) => setNuevoCliente({...nuevoCliente, telefono: e.target.value})}
                    />
                    <select
                      value={nuevoCliente.documento.tipo_documento}
                      onChange={(e) => setNuevoCliente({
                        ...nuevoCliente,
                        documento: {...nuevoCliente.documento, tipo_documento: e.target.value}
                      })}
                    >
                      <option value="DNI">DNI</option>
                      <option value="Pasaporte">Pasaporte</option>
                      <option value="RUC">RUC</option>
                      <option value="Carnet Extranjeria">Carnet Extranjería</option>
                    </select>
                    <input
                      type="text"
                      placeholder="Número de Documento"
                      value={nuevoCliente.documento.numero_documento}
                      onChange={(e) => setNuevoCliente({
                        ...nuevoCliente,
                        documento: {...nuevoCliente.documento, numero_documento: e.target.value}
                      })}
                      required
                    />
                    <button type="submit">Registrar Cliente</button>
                  </form>
                </div>

                <div className="lista-section">
                  <h2>Clientes Registrados ({clientes.length})</h2>
                  <div className="lista-items">
                    {clientes.map(cliente => (
                      <div key={cliente.cliente_id} className="item-card">
                        <h3>{cliente.nombre} {cliente.apellido}</h3>
                        <p>📧 {cliente.email}</p>
                        <p>📱 {cliente.telefono}</p>
                        <p>🆔 {cliente.documentos[0]?.numero_documento}</p>
                        <span className={`badge ${cliente.estado}`}>{cliente.estado}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* VISTA CUENTAS */}
            {vista === 'cuentas' && (
              <div className="vista-container">
                <div className="formulario-section">
                  <h2>Crear Cuenta</h2>
                  <form onSubmit={handleCrearCuenta}>
                    <select
                      value={nuevaCuenta.cliente_id}
                      onChange={(e) => setNuevaCuenta({...nuevaCuenta, cliente_id: e.target.value})}
                      required
                    >
                      <option value="">Seleccionar cliente</option>
                      {clientes.map(cliente => (
                        <option key={cliente.cliente_id} value={cliente.cliente_id}>
                          ID: {cliente.cliente_id} - {cliente.nombre} {cliente.apellido} ({cliente.email})
                        </option>
                      ))}
                    </select>
                    <select
                      value={nuevaCuenta.tipo_cuenta_id}
                      onChange={(e) => setNuevaCuenta({...nuevaCuenta, tipo_cuenta_id: e.target.value})}
                      required
                    >
                      <option value="">Seleccionar tipo de cuenta</option>
                      {tiposCuenta.map(tipo => (
                        <option key={tipo.tipo_cuenta_id} value={tipo.tipo_cuenta_id}>
                          {tipo.nombre} - {tipo.descripcion}
                        </option>
                      ))}
                    </select>
                    <input
                      type="number"
                      placeholder="Saldo inicial"
                      value={nuevaCuenta.saldo}
                      onChange={(e) => setNuevaCuenta({...nuevaCuenta, saldo: e.target.value})}
                      step="0.01"
                    />
                    <select
                      value={nuevaCuenta.moneda}
                      onChange={(e) => setNuevaCuenta({...nuevaCuenta, moneda: e.target.value})}
                    >
                      <option value="PEN">PEN (Soles)</option>
                      <option value="USD">USD (Dólares)</option>
                      <option value="EUR">EUR (Euros)</option>
                    </select>
                    <button type="submit">Crear Cuenta</button>
                  </form>
                </div>

                <div className="lista-section">
                  <h2>Cuentas Activas ({cuentas.length})</h2>
                  <div className="lista-items">
                    {cuentas.map(cuenta => (
                      <div key={cuenta.cuenta_id} className="item-card">
                        <h3>💳 {cuenta.numero_cuenta}</h3>
                        <p><strong>{cuenta.tipo_cuenta_nombre}</strong></p>
                        <p>Cliente ID: {cuenta.cliente_id}</p>
                        <p className="saldo">Saldo: {cuenta.moneda} {parseFloat(cuenta.saldo).toFixed(2)}</p>
                        <span className={`badge ${cuenta.estado}`}>{cuenta.estado}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* VISTA TRANSACCIONES */}
            {vista === 'transacciones' && (
              <div className="vista-container">
                <div className="formulario-section">
                  <h2>Nueva Transacción</h2>
                  <form onSubmit={handleCrearTransaccion}>
                    <select
                      value={nuevaTransaccion.tipo}
                      onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, tipo: e.target.value})}
                    >
                      <option value="DEPOSITO">Depósito</option>
                      <option value="RETIRO">Retiro</option>
                      <option value="TRANSFERENCIA">Transferencia</option>
                      <option value="PAGO_SERVICIO">Pago de Servicio</option>
                    </select>

                    {(nuevaTransaccion.tipo === 'RETIRO' || nuevaTransaccion.tipo === 'TRANSFERENCIA') && (
                      <select
                        value={nuevaTransaccion.cuentaOrigenId}
                        onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, cuentaOrigenId: e.target.value})}
                        required
                      >
                        <option value="">Seleccionar cuenta origen</option>
                        {cuentas.map(cuenta => (
                          <option key={cuenta.cuenta_id} value={cuenta.cuenta_id}>
                            💳 {cuenta.numero_cuenta} - {cuenta.tipo_cuenta_nombre} - Saldo: {cuenta.moneda} {parseFloat(cuenta.saldo).toFixed(2)}
                          </option>
                        ))}
                      </select>
                    )}

                    {(nuevaTransaccion.tipo === 'DEPOSITO' || nuevaTransaccion.tipo === 'TRANSFERENCIA') && (
                      <select
                        value={nuevaTransaccion.cuentaDestinoId}
                        onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, cuentaDestinoId: e.target.value})}
                        required
                      >
                        <option value="">Seleccionar cuenta destino</option>
                        {cuentas.map(cuenta => (
                          <option key={cuenta.cuenta_id} value={cuenta.cuenta_id}>
                            💳 {cuenta.numero_cuenta} - {cuenta.tipo_cuenta_nombre} - Saldo: {cuenta.moneda} {parseFloat(cuenta.saldo).toFixed(2)}
                          </option>
                        ))}
                      </select>
                    )}

                    <input
                      type="number"
                      placeholder="Monto"
                      value={nuevaTransaccion.monto}
                      onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, monto: e.target.value})}
                      step="0.01"
                      required
                    />
                    <select
                      value={nuevaTransaccion.moneda}
                      onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, moneda: e.target.value})}
                    >
                      <option value="PEN">PEN</option>
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                    </select>
                    <input
                      type="text"
                      placeholder="Descripción"
                      value={nuevaTransaccion.descripcion}
                      onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, descripcion: e.target.value})}
                    />
                    <button type="submit">Realizar Transacción</button>
                  </form>
                </div>

                <div className="lista-section">
                  <h2>Transacciones Recientes ({transacciones.length})</h2>
                  <div className="lista-items">
                    {transacciones.slice(0, 20).map(tx => (
                      <div key={tx.id} className="item-card">
                        <h3>🔖 {tx.transaccionId}</h3>
                        <p><strong>{tx.tipo}</strong></p>
                        <p>Monto: {tx.moneda} {parseFloat(tx.monto).toFixed(2)}</p>
                        <p>{tx.descripcion}</p>
                        <p className="fecha">{new Date(tx.fecha).toLocaleString()}</p>
                        <span className={`badge ${tx.estado.toLowerCase()}`}>{tx.estado}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* VISTA ANALYTICS */}
            {vista === 'analytics' && (
              <div className="vista-container analytics-view">
                <h2>📊 Analytics - DataLake Dashboard</h2>
                <p className="subtitle">Análisis de datos desde Amazon Athena (consultas pueden tomar 5-10 segundos)</p>

                {/* Dashboard Ejecutivo */}
                {dashboardData && Object.keys(dashboardData).length > 0 && (
                  <div className="dashboard-grid">
                    <h3>Resumen Ejecutivo</h3>
                    <div className="metrics-cards">
                      <div className="metric-card">
                        <h4>👥 Clientes</h4>
                        <p className="metric-value">{dashboardData.total_clientes || dashboardData.clientes_activos || '0'}</p>
                      </div>
                      <div className="metric-card">
                        <h4>💳 Cuentas</h4>
                        <p className="metric-value">{dashboardData.total_cuentas || '0'}</p>
                      </div>
                      <div className="metric-card">
                        <h4>💸 Transacciones</h4>
                        <p className="metric-value">{dashboardData.total_transacciones || '0'}</p>
                      </div>
                      <div className="metric-card">
                        <h4>💰 Volumen Total</h4>
                        <p className="metric-value">
                          {dashboardData.moneda_principal || 'PEN'} {parseFloat(dashboardData.volumen_transaccional || dashboardData.saldo_total_banco || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}
                        </p>
                      </div>
                      <div className="metric-card">
                        <h4>📊 Saldo Promedio</h4>
                        <p className="metric-value">
                          {dashboardData.moneda_principal || 'PEN'} {parseFloat(dashboardData.saldo_promedio || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}
                        </p>
                      </div>
                      <div className="metric-card">
                        <h4>💵 Transacción Promedio</h4>
                        <p className="metric-value">
                          {dashboardData.moneda_principal || 'PEN'} {parseFloat(dashboardData.transacción_promedio || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Resumen de Cuentas */}
                {cuentasAnalytics && (
                  <div className="analytics-section">
                    <h3>Análisis de Cuentas</h3>
                    <div className="stats-grid">
                      {(cuentasAnalytics.results || cuentasAnalytics.data || []).map((cuenta, idx) => (
                        <div key={idx} className="stat-card">
                          <h4>{cuenta.tipo_cuenta || cuenta.nombre_tipo || 'N/A'}</h4>
                          <p>Total: <strong>{cuenta.cantidad || cuenta.cantidad_cuentas || '0'}</strong> cuentas</p>
                          <p>Saldo Total: <strong>PEN {parseFloat(cuenta.saldo_total || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</strong></p>
                          <p>Promedio: PEN {parseFloat(cuenta.saldo_promedio || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Resumen de Transacciones */}
                {transaccionesAnalytics && (
                  <div className="analytics-section">
                    <h3>Análisis de Transacciones</h3>
                    <div className="stats-grid">
                      {(transaccionesAnalytics.results || transaccionesAnalytics.data || []).map((tx, idx) => (
                        <div key={idx} className="stat-card">
                          <h4>{tx.tipo || 'N/A'}</h4>
                          <p>Cantidad: <strong>{tx.cantidad || tx.total_transacciones || '0'}</strong></p>
                          <p>Monto Total: <strong>PEN {parseFloat(tx.monto_total || tx.volumen_total || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</strong></p>
                          <p>Promedio: PEN {parseFloat(tx.monto_promedio || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Clientes VIP */}
                {clientesVIP.length > 0 && (
                  <div className="analytics-section">
                    <h3>🌟 Clientes VIP (Patrimonio {'>'} 10,000)</h3>
                    <div className="lista-items">
                      {clientesVIP.map((cliente, idx) => (
                        <div key={idx} className="item-card vip">
                          <h4>👤 {cliente.nombre} {cliente.apellido}</h4>
                          <p>📧 {cliente.email}</p>
                          <p>💳 Cuentas: <strong>{cliente.total_cuentas}</strong></p>
                          <p>💰 Patrimonio Total: <strong>PEN {parseFloat(cliente.patrimonio_total).toLocaleString('es-PE', {minimumFractionDigits: 2})}</strong></p>
                          <p>📊 Saldo Promedio: PEN {parseFloat(cliente.saldo_promedio).toLocaleString('es-PE', {minimumFractionDigits: 2})}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {!dashboardData && !loading && (
                  <div className="empty-state">
                    <p>📊 Haz clic en "Analytics" para cargar el dashboard</p>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </main>

      <footer className="App-footer">
        <p>Cloud Bank © 2024 - Microservicios en AWS</p>
      </footer>
    </div>
  );
}

export default App;
