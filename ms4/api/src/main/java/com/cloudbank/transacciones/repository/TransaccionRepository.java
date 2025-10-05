package com.cloudbank.transacciones.repository;

import com.cloudbank.transacciones.model.Transaccion;
import com.cloudbank.transacciones.model.Transaccion.EstadoTransaccion;
import com.cloudbank.transacciones.model.Transaccion.TipoTransaccion;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface TransaccionRepository extends MongoRepository<Transaccion, String> {

    Optional<Transaccion> findByTransaccionId(String transaccionId);

    List<Transaccion> findByCuentaOrigenId(Integer cuentaOrigenId);

    List<Transaccion> findByCuentaDestinoId(Integer cuentaDestinoId);

    List<Transaccion> findByCuentaOrigenIdOrCuentaDestinoId(Integer cuentaOrigenId, Integer cuentaDestinoId);

    List<Transaccion> findByTipo(TipoTransaccion tipo);

    List<Transaccion> findByEstado(EstadoTransaccion estado);

    List<Transaccion> findByFechaBetween(LocalDateTime inicio, LocalDateTime fin);

    List<Transaccion> findByCuentaOrigenIdAndFechaBetween(Integer cuentaOrigenId, LocalDateTime inicio, LocalDateTime fin);
}
