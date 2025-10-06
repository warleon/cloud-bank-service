"""
API REST para Consultas Analíticas del DataLake
Ejecuta queries en Athena y devuelve resultados en JSON
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

from athena_client import AthenaClient
from queries import PREDEFINED_QUERIES

# Cargar variables de entorno
load_dotenv()

# Configurar logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Cloud Bank DataLake Analytics API",
    description="API REST para consultas analíticas sobre el DataLake del sistema bancario Cloud Bank",
    version="2.0.0"
)

# Configurar CORS (para permitir acceso desde navegadores)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente de Athena
athena_client = AthenaClient()


# Modelos Pydantic
class CustomQueryRequest(BaseModel):
    query: str
    database: str = "cloud_bank_db"


class QueryResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    rows_count: Optional[int] = None
    execution_time_ms: Optional[int] = None
    error: Optional[str] = None


# ========== ENDPOINTS ==========

@app.get("/", tags=["Health"])
async def root():
    """Endpoint raíz - Health check"""
    return {
        "service": "Cloud Bank DataLake Analytics API",
        "status": "running",
        "version": "2.0.0",
        "description": "API de consultas analíticas para Cloud Bank",
        "endpoints": {
            "clientes": "/api/clientes/*",
            "cuentas": "/api/cuentas/*",
            "transacciones": "/api/transacciones/*",
            "analisis": "/api/analisis/*",
            "dashboard": "/api/dashboard"
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check del servicio"""
    try:
        # Verificar conexión con Athena
        test_query = "SELECT 1 as test"
        result = athena_client.execute_query(test_query)
        
        return {
            "status": "healthy",
            "athena_connection": "ok" if result else "error",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


# ========== CLIENTES (PostgreSQL - MS1) ==========

@app.get("/api/clientes/resumen", tags=["Clientes"], response_model=QueryResponse)
async def get_clientes_resumen():
    """Obtener resumen de clientes del banco"""
    try:
        query = PREDEFINED_QUERIES["clientes_resumen"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en clientes_resumen: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/clientes/lista", tags=["Clientes"], response_model=QueryResponse)
async def get_clientes_lista(limit: int = Query(50, ge=1, le=500)):
    """Obtener lista de clientes con sus documentos"""
    try:
        query = PREDEFINED_QUERIES["clientes_lista"].format(limit=limit)
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en clientes_lista: {e}")
        return QueryResponse(success=False, error=str(e))


# ========== CUENTAS (MySQL - MS2) ==========

@app.get("/api/cuentas/resumen", tags=["Cuentas"], response_model=QueryResponse)
async def get_cuentas_resumen():
    """Obtener resumen financiero del banco"""
    try:
        query = PREDEFINED_QUERIES["cuentas_resumen"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en cuentas_resumen: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/cuentas/por-tipo", tags=["Cuentas"], response_model=QueryResponse)
async def get_cuentas_por_tipo():
    """Obtener cuentas agrupadas por tipo"""
    try:
        query = PREDEFINED_QUERIES["cuentas_por_tipo"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en cuentas_por_tipo: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/cuentas/top-saldos", tags=["Cuentas"], response_model=QueryResponse)
async def get_cuentas_top_saldos(limit: int = Query(20, ge=1, le=100)):
    """Obtener cuentas con mayores saldos"""
    try:
        query = PREDEFINED_QUERIES["cuentas_top_saldos"].format(limit=limit)
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en cuentas_top_saldos: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/clientes/con-cuentas", tags=["Clientes"], response_model=QueryResponse)
async def get_clientes_con_cuentas(limit: int = Query(50, ge=1, le=500)):
    """Obtener clientes con sus cuentas y patrimonio total"""
    try:
        query = PREDEFINED_QUERIES["clientes_con_cuentas"].format(limit=limit)
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en clientes_con_cuentas: {e}")
        return QueryResponse(success=False, error=str(e))


# ========== TRANSACCIONES (MongoDB - MS4) ==========

@app.get("/api/transacciones/resumen", tags=["Transacciones"], response_model=QueryResponse)
async def get_transacciones_resumen():
    """Obtener resumen de transacciones"""
    try:
        query = PREDEFINED_QUERIES["transacciones_resumen"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en transacciones_resumen: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/transacciones/por-tipo", tags=["Transacciones"], response_model=QueryResponse)
async def get_transacciones_por_tipo():
    """Obtener transacciones agrupadas por tipo"""
    try:
        query = PREDEFINED_QUERIES["transacciones_por_tipo"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en transacciones_por_tipo: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/transacciones/por-estado", tags=["Transacciones"], response_model=QueryResponse)
async def get_transacciones_por_estado():
    """Obtener transacciones agrupadas por estado"""
    try:
        query = PREDEFINED_QUERIES["transacciones_por_estado"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en transacciones_por_estado: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/transacciones/recientes", tags=["Transacciones"], response_model=QueryResponse)
async def get_transacciones_recientes(limit: int = Query(50, ge=1, le=500)):
    """Obtener transacciones más recientes"""
    try:
        query = PREDEFINED_QUERIES["transacciones_recientes"].format(limit=limit)
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en transacciones_recientes: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/transacciones/detalladas", tags=["Transacciones"], response_model=QueryResponse)
async def get_transacciones_detalladas(limit: int = Query(50, ge=1, le=500)):
    """Obtener transacciones con información completa de cuentas y clientes"""
    try:
        query = PREDEFINED_QUERIES["transacciones_detalladas"].format(limit=limit)
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en transacciones_detalladas: {e}")
        return QueryResponse(success=False, error=str(e))


# ========== ANÁLISIS DE NEGOCIO ==========

@app.get("/api/analisis/clientes-vip", tags=["Análisis"], response_model=QueryResponse)
async def get_clientes_vip(
    threshold: float = Query(10000, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Obtener clientes VIP con patrimonio sobre el umbral especificado"""
    try:
        query = PREDEFINED_QUERIES["analisis_clientes_vip"].format(
            threshold=threshold,
            limit=limit
        )
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en analisis_clientes_vip: {e}")
        return QueryResponse(success=False, error=str(e))


@app.get("/api/analisis/actividad-diaria", tags=["Análisis"], response_model=QueryResponse)
async def get_actividad_transaccional_diaria():
    """Obtener actividad transaccional de los últimos 30 días"""
    try:
        query = PREDEFINED_QUERIES["actividad_transaccional_diaria"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en actividad_transaccional_diaria: {e}")
        return QueryResponse(success=False, error=str(e))


# ========== DASHBOARD EJECUTIVO BANCARIO ==========

@app.get("/api/dashboard", tags=["Dashboard"], response_model=QueryResponse)
async def get_dashboard_ejecutivo():
    """Obtener métricas clave para dashboard ejecutivo bancario"""
    try:
        query = PREDEFINED_QUERIES["dashboard_ejecutivo"]
        results = athena_client.execute_query(query)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except Exception as e:
        logger.error(f"Error en dashboard: {e}")
        return QueryResponse(success=False, error=str(e))


# ========== QUERY PERSONALIZADA ==========

@app.post("/api/query/custom", tags=["Custom"], response_model=QueryResponse)
async def execute_custom_query(request: CustomQueryRequest):
    """Ejecutar una query SQL personalizada en Athena"""
    try:
        # Validación básica de seguridad
        forbidden_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE"]
        query_upper = request.query.upper()
        
        for keyword in forbidden_keywords:
            if keyword in query_upper:
                raise HTTPException(
                    status_code=400,
                    detail=f"Keyword '{keyword}' no permitido. Solo queries de lectura (SELECT)"
                )
        
        results = athena_client.execute_query(request.query, request.database)
        
        return QueryResponse(
            success=True,
            data=results,
            rows_count=len(results) if results else 0,
            execution_time_ms=athena_client.last_execution_time_ms
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en custom query: {e}")
        return QueryResponse(success=False, error=str(e))


# ========== LISTAR QUERIES DISPONIBLES ==========

@app.get("/api/queries/list", tags=["Metadata"])
async def list_available_queries():
    """Listar todas las queries predefinidas disponibles"""
    return {
        "total_queries": len(PREDEFINED_QUERIES),
        "queries": list(PREDEFINED_QUERIES.keys())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)