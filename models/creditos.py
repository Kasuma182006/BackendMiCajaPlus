from conexion import obtenerConexion
import datetime
from flask import jsonify

class Creditos:
    
   def insertar_credito(self,idVenta,idCliente):
    conexion=obtenerConexion()
    cursor=conexion.cursor()
    cursor.execute("INSERT INTO creditos (idVentas,idCliente) VALUES (%s,%s)",
                   idVenta,idCliente)
    conexion.commit()
    resultado=cursor.rowcount
    cursor.close()
    conexion.close()
    return resultado
   
   
   


   # def consultar_creditos(self,idTendero):
   #    conexion = obtenerConexion()
   #    cursor = conexion.cursor(dictionary=True)
   #    cursor.execute("""SELECT c.cedula,c.nombre,c.telefono,SUM(o.valor) AS valor,MAX(DATE(o.fecha)) AS fecha FROM operaciones o JOIN clientes c ON o.idCliente = c.cedula
   #    WHERE o.tipo = 'venta' AND o.tipoPago = 1 AND o.valor > 0 AND o,idTendero = %s GROUP BY c.cedula, c.nombre, c.telefono HAVING SUM(o.valor) > 0;""",(idTendero))
   #    result = cursor.fetchall()
   #  # Formatear la fecha a texto (YYYY-MM-DD)
   #    for fila in result:
   #      if isinstance(fila['fecha'], (datetime.date, datetime.datetime)):
   #          fila['fecha'] = fila['fecha'].strftime("%d-%m-%Y")
   #    cursor.close()
   #    conexion.close()
   #    return result
   
   
   

   # def contar_creditos(self,datos):
   #    conexion = obtenerConexion()
   #    cursor = conexion.cursor(dictionary=True)
   #    cursor.execute("""SELECT COUNT(*) AS Ncredito
   #             FROM operaciones
   #             WHERE DATE(fecha) BETWEEN %s AND %s
   #             AND idTendero = %s
   #             AND tipo = %s
   #             AND tipoPago = %s;""",(datos['fechaInicial'], datos['fechaFin'], datos['idTendero'],'venta',1))
                                 
      
      
      
      # result = cursor.fetchone()
      # cursor.close()
      # conexion.close()
      # return result



