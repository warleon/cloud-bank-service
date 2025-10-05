package com.cloudbank.transacciones.controller;

import com.cloudbank.transacciones.model.Transaccion;
import com.cloudbank.transacciones.model.Transaccion.EstadoTransaccion;
import com.cloudbank.transacciones.model.Transaccion.TipoTransaccion;
import com.cloudbank.transacciones.service.TransaccionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/")
@CrossOrigin(origins = "*")
public class TransaccionController {

    @Autowired
    private TransaccionService transaccionService;

    @GetMapping
    public ResponseEntity<Map<String, Object>> root() {
        Map<String, Object> response = new HashMap<>();
        response.put("servicio", "MS4 - Gestión de Transacciones");
        response.put("version", "1.0.0");
        response.put("estado", "activo");
        return ResponseEntity.ok(response);
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "healthy");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/transacciones")
    public ResponseEntity<Transaccion> crearTransaccion(@Valid @RequestBody Transaccion transaccion) {
        Transaccion nuevaTransaccion = transaccionService.crearTransaccion(transaccion);
        return ResponseEntity.status(HttpStatus.CREATED).body(nuevaTransaccion);
    }

    @GetMapping("/transacciones")
    public ResponseEntity<List<Transaccion>> listarTransacciones() {
        List<Transaccion> transacciones = transaccionService.obtenerTodasTransacciones();
        return ResponseEntity.ok(transacciones);
    }

    @GetMapping("/transacciones/{id}")
    public ResponseEntity<Transaccion> obtenerTransaccion(@PathVariable String id) {
        return transaccionService.obtenerTransaccionPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/transacciones/transaccion-id/{transaccionId}")
    public ResponseEntity<Transaccion> obtenerTransaccionPorTransaccionId(@PathVariable String transaccionId) {
        return transaccionService.obtenerTransaccionPorTransaccionId(transaccionId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/transacciones/cuenta/{cuentaId}")
    public ResponseEntity<List<Transaccion>> obtenerTransaccionesPorCuenta(@PathVariable Integer cuentaId) {
        List<Transaccion> transacciones = transaccionService.obtenerTransaccionesPorCuenta(cuentaId);
        return ResponseEntity.ok(transacciones);
    }

    @GetMapping("/transacciones/tipo/{tipo}")
    public ResponseEntity<List<Transaccion>> obtenerTransaccionesPorTipo(@PathVariable TipoTransaccion tipo) {
        List<Transaccion> transacciones = transaccionService.obtenerTransaccionesPorTipo(tipo);
        return ResponseEntity.ok(transacciones);
    }

    @GetMapping("/transacciones/estado/{estado}")
    public ResponseEntity<List<Transaccion>> obtenerTransaccionesPorEstado(@PathVariable EstadoTransaccion estado) {
        List<Transaccion> transacciones = transaccionService.obtenerTransaccionesPorEstado(estado);
        return ResponseEntity.ok(transacciones);
    }

    @GetMapping("/transacciones/fecha-rango")
    public ResponseEntity<List<Transaccion>> obtenerTransaccionesPorRango(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime inicio,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime fin) {
        List<Transaccion> transacciones = transaccionService.obtenerTransaccionesPorRangoFecha(inicio, fin);
        return ResponseEntity.ok(transacciones);
    }

    @PatchMapping("/transacciones/{id}/estado")
    public ResponseEntity<Transaccion> actualizarEstado(
            @PathVariable String id,
            @RequestBody Map<String, String> body) {
        
        String estadoStr = body.get("estado");
        if (estadoStr == null) {
            return ResponseEntity.badRequest().build();
        }

        try {
            EstadoTransaccion nuevoEstado = EstadoTransaccion.valueOf(estadoStr.toUpperCase());
            Transaccion transaccionActualizada = transaccionService.actualizarEstado(id, nuevoEstado);
            
            if (transaccionActualizada != null) {
                return ResponseEntity.ok(transaccionActualizada);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @DeleteMapping("/transacciones/{id}")
    public ResponseEntity<Map<String, String>> eliminarTransaccion(@PathVariable String id) {
        if (transaccionService.obtenerTransaccionPorId(id).isPresent()) {
            transaccionService.eliminarTransaccion(id);
            Map<String, String> response = new HashMap<>();
            response.put("mensaje", "Transacción eliminada exitosamente");
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.notFound().build();
    }
}
