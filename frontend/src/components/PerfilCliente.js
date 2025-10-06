import React, { useState } from 'react';
import { getPerfilCompleto, buscarClientes } from '../api';
import './PerfilCliente.css';

function PerfilCliente() {
  const [busqueda, setBusqueda] = useState('');
  const [resultadosBusqueda, setResultadosBusqueda] = useState([]);
  const [perfilCompleto, setPerfilCompleto] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState(null);
  const [mostrarResultados, setMostrarResultados] = useState(false);

  const handleBuscar = async (e) => {
    e.preventDefault();
    if (!busqueda.trim()) {
      setMensaje({ texto: 'Por favor ingresa un término de búsqueda', tipo: 'error' });
      return;
    }

    setLoading(true);
    setMensaje(null);
    try {
      const response = await buscarClientes(busqueda);
      setResultadosBusqueda(response.data.resultados || []);
      setMostrarResultados(true);
      if (response.data.resultados.length === 0) {
        setMensaje({ texto: 'No se encontraron clientes', tipo: 'info' });
      }
    } catch (error) {
      console.error('Error buscando:', error);
      setMensaje({ texto: 'Error al buscar clientes', tipo: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleSeleccionarCliente = async (clienteId) => {
    setLoading(true);
    setMensaje(null);
    setMostrarResultados(false);
    try {
      const response = await getPerfilCompleto(clienteId);
      setPerfilCompleto(response.data);
      setBusqueda(''); // Limpiar búsqueda
      setResultadosBusqueda([]);
    } catch (error) {
      console.error('Error cargando perfil:', error);
      setMensaje({ texto: 'Error al cargar perfil del cliente', tipo: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleLimpiar = () => {
    setBusqueda('');
    setResultadosBusqueda([]);
    setPerfilCompleto(null);
    setMensaje(null);
    setMostrarResultados(false);
  };

  const formatearFecha = (fecha) => {
    if (!fecha) return 'N/A';
    return new Date(fecha).toLocaleString('es-PE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatearMoneda = (valor) => {
    return new Intl.NumberFormat('es-PE', {
      style: 'currency',
      currency: 'PEN'
    }).format(valor);
  };

  return (
    <div className="perfil-cliente-container">
      <h2>🔍 Perfil Completo del Cliente (Vista 360°)</h2>
      <p className="descripcion">Busca un cliente y visualiza toda su información: datos personales, cuentas y transacciones.</p>

      {/* Barra de búsqueda */}
      <form className="search-form" onSubmit={handleBuscar}>
        <input
          type="text"
          placeholder="Buscar por nombre, apellido o email..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="btn-buscar" disabled={loading}>
          {loading ? '🔄 Buscando...' : '🔎 Buscar'}
        </button>
        {perfilCompleto && (
          <button type="button" className="btn-limpiar" onClick={handleLimpiar}>
            🔄 Nueva Búsqueda
          </button>
        )}
      </form>

      {/* Mensajes */}
      {mensaje && (
        <div className={`mensaje ${mensaje.tipo}`}>
          {mensaje.texto}
        </div>
      )}

      {/* Resultados de búsqueda */}
      {mostrarResultados && resultadosBusqueda.length > 0 && (
        <div className="resultados-busqueda">
          <h3>📋 Resultados de búsqueda ({resultadosBusqueda.length})</h3>
          <div className="resultados-lista">
            {resultadosBusqueda.map((cliente) => (
              <div
                key={cliente.cliente_id}
                className="resultado-item"
                onClick={() => handleSeleccionarCliente(cliente.cliente_id)}
              >
                <div className="resultado-nombre">
                  <strong>{cliente.nombre} {cliente.apellido}</strong>
                  <span className={`badge ${cliente.estado === 'activo' ? 'badge-activo' : 'badge-inactivo'}`}>
                    {cliente.estado}
                  </span>
                </div>
                <div className="resultado-detalles">
                  <span>📧 {cliente.email}</span>
                  <span>📱 {cliente.telefono}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && <div className="loading">⏳ Cargando...</div>}

      {/* Perfil completo */}
      {perfilCompleto && !loading && (
        <div className="perfil-completo">
          {/* Información Personal */}
          <div className="card info-personal-card">
            <h3>👤 Información Personal</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Nombre Completo:</label>
                <span>{perfilCompleto.cliente.nombre} {perfilCompleto.cliente.apellido}</span>
              </div>
              <div className="info-item">
                <label>Email:</label>
                <span>{perfilCompleto.cliente.email}</span>
              </div>
              <div className="info-item">
                <label>Teléfono:</label>
                <span>{perfilCompleto.cliente.telefono}</span>
              </div>
              <div className="info-item">
                <label>Estado:</label>
                <span className={`badge ${perfilCompleto.cliente.estado === 'activo' ? 'badge-activo' : 'badge-inactivo'}`}>
                  {perfilCompleto.cliente.estado}
                </span>
              </div>
              <div className="info-item">
                <label>Cliente desde:</label>
                <span>{formatearFecha(perfilCompleto.cliente.fecha_registro)}</span>
              </div>
              {perfilCompleto.cliente.documentos && perfilCompleto.cliente.documentos.length > 0 && (
                <div className="info-item">
                  <label>Documento:</label>
                  <span>
                    {perfilCompleto.cliente.documentos[0].tipo_documento}: {perfilCompleto.cliente.documentos[0].numero_documento}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Resumen Financiero */}
          <div className="card resumen-financiero-card">
            <h3>💰 Resumen Financiero</h3>
            <div className="resumen-grid">
              <div className="resumen-item">
                <div className="resumen-label">Patrimonio Total</div>
                <div className="resumen-valor destaca">
                  {formatearMoneda(perfilCompleto.resumen_financiero.patrimonio_total)}
                </div>
              </div>
              <div className="resumen-item">
                <div className="resumen-label">Cuentas Activas</div>
                <div className="resumen-valor">
                  {perfilCompleto.resumen_financiero.cuentas_activas || 0} / {perfilCompleto.resumen_financiero.total_cuentas}
                </div>
              </div>
              <div className="resumen-item">
                <div className="resumen-label">Total Transacciones</div>
                <div className="resumen-valor">{perfilCompleto.resumen_financiero.total_transacciones}</div>
              </div>
              <div className="resumen-item">
                <div className="resumen-label">Última Actividad</div>
                <div className="resumen-valor-pequeno">
                  {formatearFecha(perfilCompleto.resumen_financiero.ultima_actividad)}
                </div>
              </div>
            </div>
          </div>

          {/* Cuentas */}
          <div className="card cuentas-card">
            <h3>🏦 Cuentas Bancarias ({perfilCompleto.cuentas.length})</h3>
            {perfilCompleto.cuentas.length > 0 ? (
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Número de Cuenta</th>
                      <th>Tipo</th>
                      <th>Saldo</th>
                      <th>Moneda</th>
                      <th>Estado</th>
                      <th>Fecha Apertura</th>
                    </tr>
                  </thead>
                  <tbody>
                    {perfilCompleto.cuentas.map((cuenta) => (
                      <tr key={cuenta.cuenta_id}>
                        <td><code>{cuenta.numero_cuenta}</code></td>
                        <td>{cuenta.tipo_cuenta || 'N/A'}</td>
                        <td className="numero">{formatearMoneda(cuenta.saldo)}</td>
                        <td>{cuenta.moneda}</td>
                        <td>
                          <span className={`badge ${cuenta.estado === 'activa' ? 'badge-activo' : 'badge-inactivo'}`}>
                            {cuenta.estado}
                          </span>
                        </td>
                        <td>{formatearFecha(cuenta.fecha_apertura)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="sin-datos">No hay cuentas registradas</p>
            )}
          </div>

          {/* Transacciones */}
          <div className="card transacciones-card">
            <h3>📊 Transacciones Recientes ({perfilCompleto.transacciones_recientes.length})</h3>
            {perfilCompleto.transacciones_recientes.length > 0 ? (
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Fecha</th>
                      <th>Tipo</th>
                      <th>Monto</th>
                      <th>Estado</th>
                      <th>Cuenta</th>
                      <th>Descripción</th>
                    </tr>
                  </thead>
                  <tbody>
                    {perfilCompleto.transacciones_recientes.map((trans) => (
                      <tr key={trans.transaccionId}>
                        <td><code>{trans.transaccionId}</code></td>
                        <td>{formatearFecha(trans.fecha)}</td>
                        <td>
                          <span className={`badge badge-${trans.tipo.toLowerCase()}`}>
                            {trans.tipo}
                          </span>
                        </td>
                        <td className="numero">{formatearMoneda(trans.monto)}</td>
                        <td>
                          <span className={`badge ${trans.estado === 'completada' ? 'badge-completada' : 'badge-pendiente'}`}>
                            {trans.estado}
                          </span>
                        </td>
                        <td><code>{trans.numero_cuenta || 'N/A'}</code></td>
                        <td className="descripcion">{trans.descripcion || 'Sin descripción'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="sin-datos">No hay transacciones registradas</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default PerfilCliente;
