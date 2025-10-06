package com.cloudbank.transacciones.service;

import com.cloudbank.transacciones.model.Transaccion;
import com.cloudbank.transacciones.model.Transaccion.EstadoTransaccion;
import com.cloudbank.transacciones.model.Transaccion.TipoTransaccion;
import com.cloudbank.transacciones.repository.TransaccionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class TransaccionService {

    @Autowired
    private TransaccionRepository transaccionRepository;

    public Transaccion crearTransaccion(Transaccion transaccion) {
        if (transaccion.getTransaccionId() == null || transaccion.getTransaccionId().isEmpty()) {
            transaccion.setTransaccionId("TRX" + UUID.randomUUID().toString().substring(0, 8).toUpperCase());
        }
        
        if (transaccion.getFecha() == null) {
            transaccion.setFecha(LocalDateTime.now());
        }
        
        if (transaccion.getEstado() == null) {
            transaccion.setEstado(EstadoTransaccion.COMPLETADA); // Cambiar a COMPLETADA por defecto
        }

        return transaccionRepository.save(transaccion);
    }

    public List<Transaccion> obtenerTodasTransacciones() {
        return transaccionRepository.findAll();
    }

    public Optional<Transaccion> obtenerTransaccionPorId(String id) {
        return transaccionRepository.findById(id);
    }

    public Optional<Transaccion> obtenerTransaccionPorTransaccionId(String transaccionId) {
        return transaccionRepository.findByTransaccionId(transaccionId);
    }

    public List<Transaccion> obtenerTransaccionesPorCuenta(Integer cuentaId) {
        return transaccionRepository.findByCuentaOrigenIdOrCuentaDestinoId(cuentaId, cuentaId);
    }

    public List<Transaccion> obtenerTransaccionesPorTipo(TipoTransaccion tipo) {
        return transaccionRepository.findByTipo(tipo);
    }

    public List<Transaccion> obtenerTransaccionesPorEstado(EstadoTransaccion estado) {
        return transaccionRepository.findByEstado(estado);
    }

    public List<Transaccion> obtenerTransaccionesPorRangoFecha(LocalDateTime inicio, LocalDateTime fin) {
        return transaccionRepository.findByFechaBetween(inicio, fin);
    }

    public Transaccion actualizarEstado(String id, EstadoTransaccion nuevoEstado) {
        Optional<Transaccion> transaccionOpt = transaccionRepository.findById(id);
        if (transaccionOpt.isPresent()) {
            Transaccion transaccion = transaccionOpt.get();
            transaccion.setEstado(nuevoEstado);
            return transaccionRepository.save(transaccion);
        }
        return null;
    }

    public void eliminarTransaccion(String id) {
        transaccionRepository.deleteById(id);
    }
}
