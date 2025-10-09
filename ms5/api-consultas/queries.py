"""
Queries SQL predefinidas para el API - Sistema Bancario Cloud Bank
Versión con detección automática de particiones más recientes
"""

PREDEFINED_QUERIES = {
    # ========== CLIENTES (PostgreSQL - MS1) ==========
    "clientes_resumen": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        )
        SELECT 
            COUNT(*) as total_clientes,
            COUNT(CASE WHEN estado = 'activo' THEN 1 END) as clientes_activos,
            COUNT(CASE WHEN estado = 'inactivo' THEN 1 END) as clientes_inactivos
        FROM cloud_bank_db.ms1_ms1_clientes, ultima_particion
        WHERE year = ultima_particion.max_year
          AND month = ultima_particion.max_month
          AND day = ultima_particion.max_day
    """,
    
    "clientes_lista": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        )
        SELECT 
            c.cliente_id,
            c.nombre,
            c.apellido,
            c.email,
            c.telefono,
            c.estado,
            d.tipo_documento,
            d.numero_documento
        FROM cloud_bank_db.ms1_ms1_clientes c, ultima_particion
        LEFT JOIN cloud_bank_db.ms1_ms1_documentos_identidad d 
            ON c.cliente_id = d.cliente_id
            AND d.year = ultima_particion.max_year
            AND d.month = ultima_particion.max_month
            AND d.day = ultima_particion.max_day
        WHERE c.year = ultima_particion.max_year
          AND c.month = ultima_particion.max_month
          AND c.day = ultima_particion.max_day
        ORDER BY c.fecha_registro DESC
        LIMIT {limit}
    """,
    
    # ========== CUENTAS (MySQL - MS2) ==========
    "cuentas_resumen": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        ),
        cuentas_unicas AS (
            SELECT DISTINCT cuenta_id, saldo
            FROM cloud_bank_db.ms2_ms2_cuentas, ultima_particion
            WHERE year = ultima_particion.max_year
              AND month = ultima_particion.max_month
              AND day = ultima_particion.max_day
        )
        SELECT 
            COUNT(*) as total_cuentas,
            SUM(saldo) as saldo_total_banco,
            AVG(saldo) as saldo_promedio,
            MIN(saldo) as saldo_minimo,
            MAX(saldo) as saldo_maximo
        FROM cuentas_unicas
    """,
    
    "cuentas_por_tipo": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        )
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
        CROSS JOIN ultima_particion
        WHERE c.year = ultima_particion.max_year
          AND c.month = ultima_particion.max_month
          AND c.day = ultima_particion.max_day
        GROUP BY t.nombre, t.descripcion
        ORDER BY saldo_total DESC
    """,
    
    "cuentas_top_saldos": """
        WITH ultima_particion_cuentas AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        ),
        ultima_particion_clientes AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        )
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
        CROSS JOIN ultima_particion_cuentas
        JOIN cloud_bank_db.ms1_ms1_clientes cli 
            ON c.cliente_id = cli.cliente_id
        CROSS JOIN ultima_particion_clientes
        JOIN cloud_bank_db.ms2_ms2_tipos_cuenta t 
            ON c.tipo_cuenta_id = t.tipo_cuenta_id
        WHERE c.year = ultima_particion_cuentas.max_year
          AND c.month = ultima_particion_cuentas.max_month
          AND c.day = ultima_particion_cuentas.max_day
          AND cli.year = ultima_particion_clientes.max_year
          AND cli.month = ultima_particion_clientes.max_month
          AND cli.day = ultima_particion_clientes.max_day
        ORDER BY CAST(c.saldo AS DOUBLE) DESC
        LIMIT {limit}
    """,
    
    "clientes_con_cuentas": """
        WITH ultima_particion_clientes AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        ),
        ultima_particion_cuentas AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        )
        SELECT 
            cli.cliente_id,
            cli.nombre,
            cli.apellido,
            cli.email,
            COUNT(c.cuenta_id) as total_cuentas,
            COALESCE(SUM(c.saldo), 0) as saldo_total
        FROM cloud_bank_db.ms1_ms1_clientes cli
        CROSS JOIN ultima_particion_clientes
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas c 
            ON cli.cliente_id = c.cliente_id
        CROSS JOIN ultima_particion_cuentas
        WHERE cli.year = ultima_particion_clientes.max_year
          AND cli.month = ultima_particion_clientes.max_month
          AND cli.day = ultima_particion_clientes.max_day
          AND (c.year = ultima_particion_cuentas.max_year
          AND c.month = ultima_particion_cuentas.max_month
          AND c.day = ultima_particion_cuentas.max_day OR c.cuenta_id IS NULL)
        GROUP BY cli.cliente_id, cli.nombre, cli.apellido, cli.email
        ORDER BY saldo_total DESC
        LIMIT {limit}
    """,
    
    # ========== TRANSACCIONES (MongoDB - MS4) ==========
    "transacciones_resumen": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            COUNT(*) as total_transacciones,
            SUM(CAST(monto AS DOUBLE)) as volumen_total,
            AVG(CAST(monto AS DOUBLE)) as monto_promedio,
            MIN(CAST(monto AS DOUBLE)) as monto_minimo,
            MAX(CAST(monto AS DOUBLE)) as monto_maximo,
            'PEN' as moneda
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion
        WHERE year = ultima_particion.max_year
          AND month = ultima_particion.max_month
          AND day = ultima_particion.max_day
    """,
    
    "transacciones_por_tipo": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            tipo,
            COUNT(*) as cantidad,
            SUM(CAST(monto AS DOUBLE)) as monto_total,
            AVG(CAST(monto AS DOUBLE)) as monto_promedio,
            'PEN' as moneda
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion
        WHERE year = ultima_particion.max_year
          AND month = ultima_particion.max_month
          AND day = ultima_particion.max_day
        GROUP BY tipo
        ORDER BY monto_total DESC
    """,
    
    "transacciones_por_estado": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            estado,
            COUNT(*) as cantidad_transacciones,
            SUM(monto) as monto_total,
            AVG(monto) as monto_promedio
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion
        WHERE year = ultima_particion.max_year
          AND month = ultima_particion.max_month
          AND day = ultima_particion.max_day
        GROUP BY estado
        ORDER BY cantidad_transacciones DESC
    """,
    
    "transacciones_recientes": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            transaccionid,
            tipo,
            monto,
            fecha,
            estado,
            descripcion,
            cuentaorigenid,
            cuentadestinoid
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion
        WHERE year = ultima_particion.max_year
          AND month = ultima_particion.max_month
          AND day = ultima_particion.max_day
        ORDER BY fecha DESC
        LIMIT {limit}
    """,
    
    "transacciones_detalladas": """
        WITH ultima_particion_trans AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        ),
        ultima_particion_cuentas AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        ),
        ultima_particion_clientes AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        )
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
        CROSS JOIN ultima_particion_trans
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas co 
            ON t.cuentaorigenid = co.cuenta_id
        CROSS JOIN ultima_particion_cuentas
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas cd 
            ON t.cuentadestinoid = cd.cuenta_id
        LEFT JOIN cloud_bank_db.ms1_ms1_clientes clio 
            ON co.cliente_id = clio.cliente_id
        CROSS JOIN ultima_particion_clientes
        LEFT JOIN cloud_bank_db.ms1_ms1_clientes clid 
            ON cd.cliente_id = clid.cliente_id
        WHERE t.year = ultima_particion_trans.max_year
          AND t.month = ultima_particion_trans.max_month
          AND t.day = ultima_particion_trans.max_day
          AND (co.year = ultima_particion_cuentas.max_year
          AND co.month = ultima_particion_cuentas.max_month
          AND co.day = ultima_particion_cuentas.max_day OR co.cuenta_id IS NULL)
          AND (cd.year = ultima_particion_cuentas.max_year
          AND cd.month = ultima_particion_cuentas.max_month
          AND cd.day = ultima_particion_cuentas.max_day OR cd.cuenta_id IS NULL)
          AND (clio.year = ultima_particion_clientes.max_year
          AND clio.month = ultima_particion_clientes.max_month
          AND clio.day = ultima_particion_clientes.max_day OR clio.cliente_id IS NULL)
          AND (clid.year = ultima_particion_clientes.max_year
          AND clid.month = ultima_particion_clientes.max_month
          AND clid.day = ultima_particion_clientes.max_day OR clid.cliente_id IS NULL)
        ORDER BY t.fecha DESC
        LIMIT {limit}
    """,
    
    # ========== DASHBOARD EJECUTIVO BANCARIO ==========
    "dashboard_ejecutivo": """
        WITH ultima_particion_clientes AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        ),
        ultima_particion_cuentas AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        ),
        ultima_particion_trans AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            'Total Clientes' as metrica,
            CAST(COUNT(DISTINCT cliente_id) AS VARCHAR) as valor,
            'clientes' as categoria
        FROM cloud_bank_db.ms1_ms1_clientes, ultima_particion_clientes
        WHERE year = ultima_particion_clientes.max_year
          AND month = ultima_particion_clientes.max_month
          AND day = ultima_particion_clientes.max_day
        
        UNION ALL
        
        SELECT 
            'Total Cuentas' as metrica,
            CAST(COUNT(DISTINCT cuenta_id) AS VARCHAR) as valor,
            'cuentas' as categoria
        FROM cloud_bank_db.ms2_ms2_cuentas, ultima_particion_cuentas
        WHERE year = ultima_particion_cuentas.max_year
          AND month = ultima_particion_cuentas.max_month
          AND day = ultima_particion_cuentas.max_day
        
        UNION ALL
        
        SELECT 
            'Saldo Total Banco' as metrica,
            CAST(ROUND(SUM(saldo_unico), 2) AS VARCHAR) as valor,
            'cuentas' as categoria
        FROM (
            SELECT DISTINCT cuenta_id, CAST(saldo AS DOUBLE) as saldo_unico
            FROM cloud_bank_db.ms2_ms2_cuentas, ultima_particion_cuentas
            WHERE saldo IS NOT NULL
              AND year = ultima_particion_cuentas.max_year
              AND month = ultima_particion_cuentas.max_month
              AND day = ultima_particion_cuentas.max_day
        )
        
        UNION ALL
        
        SELECT 
            'Total Transacciones' as metrica,
            CAST(COUNT(DISTINCT transaccionid) AS VARCHAR) as valor,
            'transacciones' as categoria
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion_trans
        WHERE year = ultima_particion_trans.max_year
          AND month = ultima_particion_trans.max_month
          AND day = ultima_particion_trans.max_day
        
        UNION ALL
        
        SELECT 
            'Volumen Transaccional' as metrica,
            CAST(ROUND(SUM(CAST(monto AS DOUBLE)), 2) AS VARCHAR) as valor,
            'transacciones' as categoria
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion_trans
        WHERE monto IS NOT NULL
          AND year = ultima_particion_trans.max_year
          AND month = ultima_particion_trans.max_month
          AND day = ultima_particion_trans.max_day
        
        UNION ALL
        
        SELECT 
            'Clientes Activos' as metrica,
            CAST(COUNT(DISTINCT cliente_id) AS VARCHAR) as valor,
            'clientes' as categoria
        FROM cloud_bank_db.ms1_ms1_clientes, ultima_particion_clientes
        WHERE estado = 'activo'
          AND year = ultima_particion_clientes.max_year
          AND month = ultima_particion_clientes.max_month
          AND day = ultima_particion_clientes.max_day
        
        UNION ALL
        
        SELECT 
            'Saldo Promedio' as metrica,
            CAST(ROUND(AVG(saldo_unico), 2) AS VARCHAR) as valor,
            'cuentas' as categoria
        FROM (
            SELECT DISTINCT cuenta_id, CAST(saldo AS DOUBLE) as saldo_unico
            FROM cloud_bank_db.ms2_ms2_cuentas, ultima_particion_cuentas
            WHERE saldo IS NOT NULL
              AND year = ultima_particion_cuentas.max_year
              AND month = ultima_particion_cuentas.max_month
              AND day = ultima_particion_cuentas.max_day
        )
        
        UNION ALL
        
        SELECT 
            'Transacción Promedio' as metrica,
            CAST(ROUND(AVG(monto_unico), 2) AS VARCHAR) as valor,
            'transacciones' as categoria
        FROM (
            SELECT DISTINCT transaccionid, CAST(monto AS DOUBLE) as monto_unico
            FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion_trans
            WHERE monto IS NOT NULL
              AND year = ultima_particion_trans.max_year
              AND month = ultima_particion_trans.max_month
              AND day = ultima_particion_trans.max_day
        )
    """,
    
    # ========== ANÁLISIS DE NEGOCIO ==========
    "analisis_clientes_vip": """
        WITH ultima_particion_clientes AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms1_ms1_clientes
        ),
        ultima_particion_cuentas AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms2_ms2_cuentas
        ),
        ultima_particion_trans AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            cli.cliente_id,
            cli.nombre,
            cli.apellido,
            cli.email,
            COUNT(c.cuenta_id) as total_cuentas,
            SUM(c.saldo) as patrimonio_total,
            COUNT(t.transaccionid) as total_transacciones
        FROM cloud_bank_db.ms1_ms1_clientes cli
        CROSS JOIN ultima_particion_clientes
        LEFT JOIN cloud_bank_db.ms2_ms2_cuentas c 
            ON cli.cliente_id = c.cliente_id
        CROSS JOIN ultima_particion_cuentas
        LEFT JOIN cloud_bank_db.ms4_ms4_transacciones t 
            ON (c.cuenta_id = t.cuentaorigenid OR c.cuenta_id = t.cuentadestinoid)
        CROSS JOIN ultima_particion_trans
        WHERE cli.year = ultima_particion_clientes.max_year
          AND cli.month = ultima_particion_clientes.max_month
          AND cli.day = ultima_particion_clientes.max_day
          AND (c.year = ultima_particion_cuentas.max_year
          AND c.month = ultima_particion_cuentas.max_month
          AND c.day = ultima_particion_cuentas.max_day OR c.cuenta_id IS NULL)
          AND (t.year = ultima_particion_trans.max_year
          AND t.month = ultima_particion_trans.max_month
          AND t.day = ultima_particion_trans.max_day OR t.transaccionid IS NULL)
        GROUP BY cli.cliente_id, cli.nombre, cli.apellido, cli.email
        HAVING SUM(c.saldo) > {threshold}
        ORDER BY patrimonio_total DESC
        LIMIT {limit}
    """,
    
    "actividad_transaccional_diaria": """
        WITH ultima_particion AS (
            SELECT MAX(year) as max_year, MAX(month) as max_month, MAX(day) as max_day
            FROM cloud_bank_db.ms4_ms4_transacciones
        )
        SELECT 
            DATE_FORMAT(fecha, '%Y-%m-%d') as fecha,
            tipo,
            COUNT(*) as cantidad,
            SUM(monto) as monto_total
        FROM cloud_bank_db.ms4_ms4_transacciones, ultima_particion
        WHERE fecha >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
          AND year = ultima_particion.max_year
          AND month = ultima_particion.max_month
          AND day = ultima_particion.max_day
        GROUP BY DATE_FORMAT(fecha, '%Y-%m-%d'), tipo
        ORDER BY fecha DESC, monto_total DESC
    """
}
