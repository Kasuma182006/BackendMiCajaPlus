from conexion import obtenerConexion

# terminar esto

class Estadisticas:

    def obtener_estadisticas(self,idTendero,fechaInicial,fechaFin):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""SELECT
        (SELECT SUM(valor) FROM ventas 
        WHERE idTendero = %s AND tipoPago = "efectivo" AND fecha BETWEEN %s AND %s) AS ventas,
                       
        (SELECT SUM(valor) FROM ventas
        WHERE idTendero = %s AND tipoPago = "credito" AND fecha BETWEEN %s AND %s) AS valorCredito,               
                       
        (SELECT COUNT(idVentas) FROM ventas
        WHERE idTendero = %s AND tipoPago = "credito" AND fecha BETWEEN %s AND %s) AS ncreditos,

        (SELECT SUM(valor) FROM costos 
        WHERE idTendero = %s AND fecha BETWEEN %s AND %s) AS costos,

        (SELECT SUM(valor) FROM gastos 
        WHERE idTendero = %s AND fecha BETWEEN %s AND %s) AS gastos;""",
        (idTendero,fechaInicial,fechaFin,
        idTendero,fechaInicial,fechaFin,
        idTendero,fechaInicial,fechaFin,
        idTendero,fechaInicial,fechaFin,
        idTendero,fechaInicial,fechaFin))
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
    

