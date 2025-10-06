"""
Queries SQL predefinidas para el API - Sistema Bancario Cloud Bank
"""

PREDEFINED_QUE    "transacciones_resumen": """
        SELECT 
            COUNT(*) as total_transacciones,
            SUM(CAST(monto AS DOUBLE)) as volumen_total,
            AVG(CAST(monto AS DOUBLE)) as monto_promedio,
            MIN(CAST(monto AS DOUBLE)) as monto_minimo,
            MAX(CAST(monto AS DOUBLE)) as monto_maximo,
            'PEN' as moneda
        FROM cloud_bank_db.ms4_ms4_transacciones
    """,
    # ========== CLIENTES (PostgreSQL - MS1) ==========
    "clientes_resumen": """
        SELECT 
            COUNT(*) as total_clientes,
            COUNT(CASE WHEN estado = 'activo' THEN 1 END) as clientes_activos,
            COUNT(CASE WHEN estado = 'inactivo' THEN 1 END) as clientes_inactivos
        FROM cloud_bank_db.ms1_ms1_clientes
    """,
    
    
    "clientes_lista": """
        SELECT 
            c.cliente_id,
            c.nombre,
            c.apellido,
            c.email,
            c.telefono,
            c.estado,
            d.tipo_documento,
            d.numero_documento
        FROM cloud_bank_db.ms1_ms1_clientes c
        LEFT JOIN cloud_bank_db.ms1_ms1_documentos_identidad d 
            ON c.cliente_id = d.cliente_id
        ORDER BY c.fecha_registro DESC
        LIMIT {limit}
    """,
    
    # ========== CUENTAS (MySQL - MS2) ==========
    "cuentas_resumen": """
        SELECT 
            COUNT(*) as total_cuentas,
            SUM(saldo) as saldo_total_banco,
            AVG(saldo) as saldo_promedio,
            MIN(saldo) as saldo_minimo,
            MAX(saldo) as saldo_maximo
        FROM cloud_bank_db.ms2_ms2_cuentas
    """,
    
    "cuentas_por_tipo": """
        SELECT 
            t.nombre as tipo_cuenta,
            t.descripcion,
            COUNT(c.cuenta_id) as cantidad_cuentas,
            COALESCE(SUM(CAST(c.saldo AS DOUBLE)), 0) as saldo_total,
            COALESCE(AVG(CAST(c.saldo AS DOUBLE)), 0) as saldo_promedio,
            'PEN' as moneda
        FROM cloud_bank_db.ms2_ms2_tipos_cuenta t
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas c 
            ON t.tipo_cuenta_id = c.tipo_cuenta_id
        GROUP BY t.nombre, t.descripcion
        ORDER BY saldo_total DESC
    """,
    
    "cuentas_top_saldos": """
        SELECT 
            c.numero_cuenta,
            cli.nombre,
            cli.apellido,
            cli.email,
            CAST(c.saldo AS DOUBLE) as saldo,
            c.moneda,
            t.nombre as tipo_cuenta,
            c.fecha_apertura
        FROM cloud_bank_db.ms2_ms2_cuentas c
        JOIN cloud_bank_db.ms1_ms1_clientes cli 
            ON c.cliente_id = cli.cliente_id
        JOIN cloud_bank_db.ms2_ms2_tipos_cuenta t 
            ON c.tipo_cuenta_id = t.tipo_cuenta_id
        ORDER BY CAST(c.saldo AS DOUBLE) DESC
        LIMIT {limit}
    """,
    
    "clientes_con_cuentas": """
        SELECT 
            cli.cliente_id,
            cli.nombre,
            cli.apellido,
            cli.email,
            COUNT(c.cuenta_id) as total_cuentas,
            COALESCE(SUM(c.saldo), 0) as saldo_total
        FROM cloud_bank_db.ms1_ms1_clientes cli
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas c 
            ON cli.cliente_id = c.cliente_id
        GROUP BY cli.cliente_id, cli.nombre, cli.apellido, cli.email
        ORDER BY saldo_total DESC
        LIMIT {limit}
    """,
    
    # ========== TRANSACCIONES (MongoDB - MS4) ==========
    "transacciones_resumen": """
        SELECT 
            COUNT(*) as total_transacciones,
            SUM(monto) as monto_total,
            AVG(monto) as monto_promedio,
            MIN(monto) as monto_minimo,
            MAX(monto) as monto_maximo
        FROM cloud_bank_db.ms4_ms4_transacciones
    """,
    
    "transacciones_por_tipo": """
        SELECT 
            tipo,
            COUNT(*) as cantidad,
            SUM(CAST(monto AS DOUBLE)) as monto_total,
            AVG(CAST(monto AS DOUBLE)) as monto_promedio,
            'PEN' as moneda
        FROM cloud_bank_db.ms4_ms4_transacciones
        GROUP BY tipo
        ORDER BY monto_total DESC
    """,
    
    "transacciones_por_estado": """
        SELECT 
            estado,
            COUNT(*) as cantidad_transacciones,
            SUM(monto) as monto_total,
            AVG(monto) as monto_promedio
        FROM cloud_bank_db.ms4_ms4_transacciones
        GROUP BY estado
        ORDER BY cantidad_transacciones DESC
    """,
    
    "transacciones_recientes": """
        SELECT 
            transaccionid,
            tipo,
            monto,
            fecha,
            estado,
            descripcion,
            cuentaorigenid,
            cuentadestinoid
        FROM cloud_bank_db.ms4_ms4_transacciones
        ORDER BY fecha DESC
        LIMIT {limit}
    """,
    
    "transacciones_detalladas": """
        SELECT 
            t.transaccionid,
            t.tipo,
            t.monto,
            t.fecha,
            t.estado,
            t.descripcion,
            co.numero_cuenta as cuenta_origen,
            cd.numero_cuenta as cuenta_destino,
            clio.nombre as cliente_origen_nombre,
            clio.apellido as cliente_origen_apellido,
            clid.nombre as cliente_destino_nombre,
            clid.apellido as cliente_destino_apellido
        FROM cloud_bank_db.ms4_ms4_transacciones t
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas co 
            ON t.cuentaorigenid = co.cuenta_id
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas cd 
            ON t.cuentadestinoid = cd.cuenta_id
        LEFT JOIN cloud_bank_db.ms1_ms1_clientes clio 
            ON co.cliente_id = clio.cliente_id
        LEFT JOIN cloud_bank_db.ms1_ms1_clientes clid 
            ON cd.cliente_id = clid.cliente_id
        ORDER BY t.fecha DESC
        LIMIT {limit}
    """,
    
    # ========== DASHBOARD EJECUTIVO BANCARIO ==========
    "dashboard_ejecutivo": """
        SELECT 
            'Total Clientes' as metrica,
            CAST(COUNT(*) AS VARCHAR) as valor,
            'clientes' as categoria
        FROM cloud_bank_db.ms1_ms1_clientes
        
        UNION ALL
        
        SELECT 
            'Total Cuentas' as metrica,
            CAST(COUNT(*) AS VARCHAR) as valor,
            'cuentas' as categoria
        FROM cloud_bank_db.ms2_ms2_cuentas
        
        UNION ALL
        
        SELECT 
            'Saldo Total Banco' as metrica,
            CAST(ROUND(SUM(saldo), 2) AS VARCHAR) as valor,
            'cuentas' as categoria
        FROM cloud_bank_db.ms2_ms2_cuentas
        
        UNION ALL
        
        SELECT 
            'Total Transacciones' as metrica,
            CAST(COUNT(*) AS VARCHAR) as valor,
            'transacciones' as categoria
        FROM cloud_bank_db.ms4_ms4_transacciones
        
        UNION ALL
        
        SELECT 
            'Volumen Transaccional' as metrica,
            CAST(ROUND(SUM(monto), 2) AS VARCHAR) as valor,
            'transacciones' as categoria
        FROM cloud_bank_db.ms4_ms4_transacciones
        
        UNION ALL
        
        SELECT 
            'Clientes Activos' as metrica,
            CAST(COUNT(*) AS VARCHAR) as valor,
            'clientes' as categoria
        FROM cloud_bank_db.ms1_ms1_clientes
        WHERE estado = 'activo'
    """,
    
    # ========== ANÁLISIS DE NEGOCIO ==========
    "analisis_clientes_vip": """
        SELECT 
            cli.cliente_id,
            cli.nombre,
            cli.apellido,
            cli.email,
            COUNT(c.cuenta_id) as total_cuentas,
            SUM(c.saldo) as patrimonio_total,
            COUNT(t.transaccionid) as total_transacciones
        FROM cloud_bank_db.ms1_ms1_clientes cli
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas c 
            ON cli.cliente_id = c.cliente_id
        LEFT JOIN cloud_bank_db.ms4_ms4_transacciones t 
            ON c.cuenta_id = t.cuentaorigenid OR c.cuenta_id = t.cuentadestinoid
        GROUP BY cli.cliente_id, cli.nombre, cli.apellido, cli.email
        HAVING SUM(c.saldo) > {threshold}
        ORDER BY patrimonio_total DESC
        LIMIT {limit}
    """,
    
    "actividad_transaccional_diaria": """
        SELECT 
            DATE_FORMAT(fecha, '%Y-%m-%d') as fecha,
            tipo,
            COUNT(*) as cantidad,
            SUM(monto) as monto_total
        FROM cloud_bank_db.ms4_ms4_transacciones
        WHERE fecha >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
        GROUP BY DATE_FORMAT(fecha, '%Y-%m-%d'), tipo
        ORDER BY fecha DESC, monto_total DESC
    """
}