package com.cloudbank.transacciones.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.index.Indexed;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.time.LocalDateTime;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "transacciones")
public class Transaccion {

    @Id
    private String id;

    @Indexed(unique = true)
    @NotNull(message = "El ID de transacción es requerido")
    private String transaccionId;

    @NotNull(message = "El tipo de transacción es requerido")
    private TipoTransaccion tipo;

    private Integer cuentaOrigenId;

    private Integer cuentaDestinoId;

    @NotNull(message = "El monto es requerido")
    @Positive(message = "El monto debe ser positivo")
    private Double monto;

    @NotNull(message = "La moneda es requerida")
    private String moneda = "PEN";

    private String descripcion;

    private LocalDateTime fecha = LocalDateTime.now();

    @NotNull(message = "El estado es requerido")
    private EstadoTransaccion estado = EstadoTransaccion.PENDIENTE;

    private Map<String, Object> metadata;

    public enum TipoTransaccion {
        DEPOSITO,
        RETIRO,
        TRANSFERENCIA,
        PAGO_SERVICIO
    }

    public enum EstadoTransaccion {
        PENDIENTE,
        COMPLETADA,
        FALLIDA,
        CANCELADA
    }
}
