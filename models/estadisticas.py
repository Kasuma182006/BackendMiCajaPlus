from conexion import obtenerConexion

# terminar esto

class Estadisticas:

    def obtener_estadisticas(self,idTendero,fechaInicial,fechaFin):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""SELECT
        COALESCE((SELECT SUM(valor) FROM ventas 
        WHERE idTendero = %s AND tipoPago = 'efectivo' AND fecha BETWEEN %s AND %s), 0) AS ventas,
                        
        COALESCE((SELECT SUM(valor) FROM ventas
        WHERE idTendero = %s AND tipoPago = 'credito' AND fecha BETWEEN %s AND %s), 0) AS valorCredito,               
                        
        COALESCE((SELECT COUNT(idVentas) FROM ventas
        WHERE idTendero = %s AND tipoPago = 'credito' AND fecha BETWEEN %s AND %s), 0) AS ncreditos,

        COALESCE((SELECT SUM(valor) FROM costos 
        WHERE idTendero = %s AND fecha BETWEEN %s AND %s), 0) AS costos,

        COALESCE((SELECT SUM(valor) FROM gastos 
        WHERE idTendero = %s AND fecha BETWEEN %s AND %s), 0) AS gastos;""",
        (idTendero, fechaInicial, fechaFin, 
        idTendero, fechaInicial, fechaFin, 
        idTendero, fechaInicial, fechaFin, 
        idTendero, fechaInicial, fechaFin, 
        idTendero, fechaInicial, fechaFin))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado
    
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
    

