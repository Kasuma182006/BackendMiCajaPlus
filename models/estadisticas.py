from conexion import obtenerConexion


class Estadisticas:
    def obtener_estadisticas(self, data):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN tipo = 'venta' THEN valor ELSE 0 END) AS ventas,
                SUM(CASE WHEN tipo = 'gasto' THEN valor ELSE 0 END) AS gastos,
                SUM(CASE WHEN tipo = 'costo' THEN valor ELSE 0 END) AS costos
            FROM operaciones
            WHERE fecha BETWEEN %s AND %s
              AND idTendero = %s
            """,
            (data['fechaInicial'], data['fechaFin'], data['idTendero'])
        )
        resultado = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultado
    
    def fecha_min (self, datafecha):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT MIN(fecha) AS primer_fecha 
            FROM operaciones  
            WHERE idTendero = %s

            """,
            (datafecha['idTendero'],)
        )
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado
    

