from conexion import obtenerConexion


class Estadisticas:

    def obtener_estadisticas(self, idTendero, fechaInicial, fechaFin):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
            IFNULL((SELECT SUM(valor) 
                FROM ventas 
                WHERE idTendero = %s 
                AND tipoPago = 'efectivo'
                AND DATE(fecha) BETWEEN %s AND %s),0) AS ventas,

            IFNULL((SELECT SUM(valor) 
                FROM ventas 
                WHERE idTendero = %s 
                AND tipoPago = 'credito'
                AND DATE(fecha) BETWEEN %s AND %s),0) AS valorCredito,

            IFNULL((SELECT COUNT(idVentas) 
                FROM ventas 
                WHERE idTendero = %s 
                AND tipoPago = 'credito'
                AND DATE(fecha) BETWEEN %s AND %s),0) AS ncreditos,

            IFNULL((SELECT SUM(valor) 
                FROM costos 
                WHERE idTendero = %s 
                AND DATE(fecha) BETWEEN %s AND %s),0) AS costos,

            IFNULL((SELECT SUM(valor) 
                FROM gastos 
                WHERE idTendero = %s 
                AND DATE(fecha) BETWEEN %s AND %s),0) AS gastos
        """,
        (
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin
        ))

        resultado = cursor.fetchone()

        # calcular utilidad
        utilidad = resultado["ventas"] - resultado["costos"] - resultado["gastos"]
        resultado["utilidad"] = utilidad

        cursor.close()
        conexion.close()

        return resultado


    def obtener_historial(self, idTendero, fechaInicial, fechaFin):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 'Venta Efectivo' AS tipo, mensaje, fecha
            FROM ventas
            WHERE idTendero=%s 
            AND LOWER(tipoPago)='efectivo'
            AND DATE(fecha) BETWEEN %s AND %s

            UNION ALL

            SELECT 'Crédito' AS tipo, mensaje, fecha
            FROM ventas
            WHERE idTendero=%s 
            AND LOWER(tipoPago)='credito'
            AND DATE(fecha) BETWEEN %s AND %s

            UNION ALL

            SELECT 'Costo' AS tipo, mensaje, fecha
            FROM costos
            WHERE idTendero=%s 
            AND DATE(fecha) BETWEEN %s AND %s

            UNION ALL

            SELECT 'Gasto' AS tipo, mensaje, fecha
            FROM gastos
            WHERE idTendero=%s 
            AND DATE(fecha) BETWEEN %s AND %s

            ORDER BY fecha ASC
        """, (
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin,
            idTendero, fechaInicial, fechaFin
        ))

        resultado = cursor.fetchall()

        cursor.close()
        conexion.close()

        return resultado


    def obtener_reporte_rango(self, idTendero, fechaInicio, fechaFin):
        conexion = obtenerConexion()
        # Aseguramos que idTendero sea un entero si tu DB así lo requiere
        try:
            id_t = int(idTendero)
        except:
            id_t = idTendero 

        cursor = conexion.cursor(dictionary=True)

        # Nota: He limpiado la estructura de la query para que sea más sólida
        query = """
            SELECT 
                (SELECT COALESCE(SUM(valor), 0) FROM ventas 
                WHERE idTendero=%s AND DATE(fecha) BETWEEN %s AND %s 
                AND tipoPago='efectivo') AS total_ventas,

                (SELECT COALESCE(SUM(valor), 0) FROM ventas 
                WHERE idTendero=%s AND DATE(fecha) BETWEEN %s AND %s 
                AND tipoPago='credito') AS total_creditos,

                (SELECT COALESCE(SUM(valor), 0) FROM costos 
                WHERE idTendero=%s AND DATE(fecha) BETWEEN %s AND %s) AS total_costos,

                (SELECT COALESCE(SUM(valor), 0) FROM gastos 
                WHERE idTendero=%s AND DATE(fecha) BETWEEN %s AND %s) AS total_gastos
        """

        params = (
            id_t, fechaInicio, fechaFin,
            id_t, fechaInicio, fechaFin,
            id_t, fechaInicio, fechaFin,
            id_t, fechaInicio, fechaFin
        )

        try:
            cursor.execute(query, params)
            resultado = cursor.fetchone()
            
            # SI RESULTADO ES NONE (aunque con COALESCE es raro, puede pasar si la query falla)
            if not resultado:
                resultado = {
                    'total_ventas': 0, 'total_creditos': 0, 
                    'total_costos': 0, 'total_gastos': 0
                }
                
            return resultado
        except Exception as e:
            print(f"DEBUG SQL ERROR: {e}") # Esto saldrá en tu terminal negra
            raise e
        finally:
            cursor.close()
            conexion.close()
#     def fecha_min (self, datafecha):
#         conexion = obtenerConexion()
#         cursor = conexion.cursor(dictionary=True)
#         cursor.execute(
#             """
#             SELECT MIN(fecha) AS primer_fecha 
#             FROM operaciones  
#             WHERE idTendero = %s

#             """,
#             (datafecha['idTendero'],)
#         )
#         resultado = cursor.fetchone()
#         cursor.close()
#         conexion.close()
#         return resultado
    

