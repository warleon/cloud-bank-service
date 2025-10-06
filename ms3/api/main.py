"""
MS3 - Servicio de Perfil Completo del Cliente (Vista 360°)
Agrega información de un cliente desde MS1, MS2 y MS4
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="MS3 - Perfil Completo del Cliente",
    description="Servicio agregador que obtiene información completa de un cliente desde MS1, MS2 y MS4",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs de otros microservicios (desde variables de entorno)
MS1_URL = os.getenv("MS1_URL", "http://localhost:5000")
MS2_URL = os.getenv("MS2_URL", "http://localhost:3000")
MS4_URL = os.getenv("MS4_URL", "http://localhost:8080")

logger.info(f"MS3 iniciado con configuración:")
logger.info(f"  MS1_URL: {MS1_URL}")
logger.info(f"  MS2_URL: {MS2_URL}")
logger.info(f"  MS4_URL: {MS4_URL}")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "servicio": "MS3 - Perfil Completo del Cliente",
        "version": "1.0.0",
        "descripcion": "Servicio agregador para obtener vista 360° de clientes",
        "endpoints": {
            "perfil_completo": "/api/clientes/{cliente_id}/perfil-completo",
            "buscar_clientes": "/api/clientes/buscar?q=Juan",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Verificar estado del servicio y conectividad con otros MS"""
    status = {
        "ms3": "healthy",
        "timestamp": datetime.now().isoformat(),
        "microservicios": {}
    }
    
    # Verificar conectividad con cada microservicio
    async with httpx.AsyncClient(timeout=5.0) as client:
        # MS1 - PostgreSQL
        try:
            await client.get(f"{MS1_URL}/clientes")
            status["microservicios"]["ms1"] = "connected"
        except Exception as e:
            status["microservicios"]["ms1"] = f"disconnected: {str(e)}"
            logger.error(f"MS1 no disponible: {e}")
        
        # MS2 - MySQL
        try:
            await client.get(f"{MS2_URL}/cuentas")
            status["microservicios"]["ms2"] = "connected"
        except Exception as e:
            status["microservicios"]["ms2"] = f"disconnected: {str(e)}"
            logger.error(f"MS2 no disponible: {e}")
        
        # MS4 - MongoDB
        try:
            await client.get(f"{MS4_URL}/transacciones")
            status["microservicios"]["ms4"] = "connected"
        except Exception as e:
            status["microservicios"]["ms4"] = f"disconnected: {str(e)}"
            logger.error(f"MS4 no disponible: {e}")
    
    return status


@app.get("/api/clientes/{cliente_id}/perfil-completo")
async def get_perfil_completo(cliente_id: int):
    """
    Obtener perfil completo de un cliente con toda su información:
    - Datos personales (MS1)
    - Cuentas bancarias (MS2)
    - Historial de transacciones (MS4)
    - Resumen financiero calculado
    """
    logger.info(f"Obteniendo perfil completo del cliente {cliente_id}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. Obtener datos del cliente desde MS1 (PostgreSQL)
            logger.info(f"Consultando MS1 para cliente {cliente_id}")
            try:
                cliente_res = await client.get(f"{MS1_URL}/clientes/{cliente_id}")
                cliente_res.raise_for_status()
                cliente_data = cliente_res.json()
                logger.info(f"Cliente obtenido: {cliente_data.get('nombre')} {cliente_data.get('apellido')}")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
                raise HTTPException(status_code=500, detail=f"Error al obtener cliente: {str(e)}")
            
            # 2. Obtener cuentas del cliente desde MS2 (MySQL)
            logger.info(f"Consultando MS2 para cuentas del cliente {cliente_id}")
            cuentas_data = []
            try:
                cuentas_res = await client.get(f"{MS2_URL}/cuentas/cliente/{cliente_id}")
                if cuentas_res.status_code == 200:
                    cuentas_data = cuentas_res.json()
                    logger.info(f"Cuentas obtenidas: {len(cuentas_data)}")
            except Exception as e:
                logger.warning(f"No se pudieron obtener cuentas: {e}")
            
            # 3. Obtener transacciones de todas las cuentas desde MS4 (MongoDB)
            logger.info(f"Consultando MS4 para transacciones del cliente {cliente_id}")
            transacciones = []
            for cuenta in cuentas_data:
                cuenta_id = cuenta.get('cuenta_id')
                try:
                    trans_res = await client.get(f"{MS4_URL}/transacciones/cuenta/{cuenta_id}")
                    if trans_res.status_code == 200:
                        trans_data = trans_res.json()
                        # Agregar número de cuenta a cada transacción para referencia
                        for trans in trans_data:
                            trans['numero_cuenta'] = cuenta.get('numero_cuenta')
                        transacciones.extend(trans_data)
                except Exception as e:
                    logger.warning(f"No se pudieron obtener transacciones de cuenta {cuenta_id}: {e}")
            
            logger.info(f"Transacciones obtenidas: {len(transacciones)}")
            
            # 4. Ordenar transacciones por fecha (más recientes primero)
            transacciones_ordenadas = sorted(
                transacciones, 
                key=lambda x: x.get('fecha', ''), 
                reverse=True
            )
            
            # 5. Calcular resumen financiero
            patrimonio_total = sum(float(c.get('saldo', 0)) for c in cuentas_data)
            ultima_actividad = transacciones_ordenadas[0].get('fecha') if transacciones_ordenadas else None
            
            resumen_financiero = {
                "patrimonio_total": round(patrimonio_total, 2),
                "moneda": "PEN",
                "total_cuentas": len(cuentas_data),
                "cuentas_activas": len([c for c in cuentas_data if c.get('estado') == 'activa']),
                "total_transacciones": len(transacciones),
                "ultima_actividad": ultima_actividad
            }
            
            # 6. Construir respuesta completa
            perfil_completo = {
                "cliente": cliente_data,
                "cuentas": cuentas_data,
                "transacciones_recientes": transacciones_ordenadas[:50],  # Últimas 50 transacciones
                "resumen_financiero": resumen_financiero
            }
            
            logger.info(f"Perfil completo generado exitosamente para cliente {cliente_id}")
            return perfil_completo
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error inesperado al obtener perfil completo: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.get("/api/clientes/buscar")
async def buscar_clientes(q: str = Query(..., min_length=1, description="Texto a buscar")):
    """
    Buscar clientes por nombre, apellido o email
    """
    logger.info(f"Buscando clientes con query: '{q}'")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # MS1 tiene el endpoint de búsqueda
            res = await client.get(f"{MS1_URL}/clientes")
            if res.status_code == 200:
                todos_clientes = res.json()
                
                # Filtrar clientes que coincidan con la búsqueda
                q_lower = q.lower()
                resultados = [
                    cliente for cliente in todos_clientes
                    if (q_lower in cliente.get('nombre', '').lower() or
                        q_lower in cliente.get('apellido', '').lower() or
                        q_lower in cliente.get('email', '').lower())
                ]
                
                logger.info(f"Búsqueda completada: {len(resultados)} resultados")
                return {
                    "query": q,
                    "total_resultados": len(resultados),
                    "resultados": resultados
                }
            else:
                raise HTTPException(status_code=500, detail="Error al buscar clientes")
                
        except Exception as e:
            logger.error(f"Error en búsqueda: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al buscar clientes: {str(e)}")


@app.get("/api/clientes/{cliente_id}/transacciones")
async def get_transacciones_cliente(
    cliente_id: int,
    limit: int = Query(50, ge=1, le=200, description="Número máximo de transacciones")
):
    """
    Obtener solo las transacciones de un cliente específico
    """
    logger.info(f"Obteniendo transacciones del cliente {cliente_id} (limit: {limit})")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. Obtener cuentas del cliente
            cuentas_res = await client.get(f"{MS2_URL}/cuentas/cliente/{cliente_id}")
            if cuentas_res.status_code != 200:
                raise HTTPException(status_code=404, detail="Cliente no encontrado o sin cuentas")
            
            cuentas_data = cuentas_res.json()
            
            # 2. Obtener transacciones de todas las cuentas
            transacciones = []
            for cuenta in cuentas_data:
                cuenta_id = cuenta.get('cuenta_id')
                try:
                    trans_res = await client.get(f"{MS4_URL}/transacciones/cuenta/{cuenta_id}")
                    if trans_res.status_code == 200:
                        trans_data = trans_res.json()
                        for trans in trans_data:
                            trans['numero_cuenta'] = cuenta.get('numero_cuenta')
                            trans['tipo_cuenta'] = cuenta.get('tipo_cuenta')
                        transacciones.extend(trans_data)
                except Exception as e:
                    logger.warning(f"Error obteniendo transacciones de cuenta {cuenta_id}: {e}")
            
            # 3. Ordenar y limitar
            transacciones_ordenadas = sorted(
                transacciones, 
                key=lambda x: x.get('fecha', ''), 
                reverse=True
            )[:limit]
            
            return {
                "cliente_id": cliente_id,
                "total_transacciones": len(transacciones),
                "transacciones_mostradas": len(transacciones_ordenadas),
                "transacciones": transacciones_ordenadas
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo transacciones: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 6000))
    uvicorn.run(app, host="0.0.0.0", port=port)
