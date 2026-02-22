from conexion import obtenerConexion

class Operaciones:
    
  def insertar_venta(self,data_venta):
    conexion=obtenerConexion()
    cursor=conexion.cursor()
    cursor.execute("INSERT INTO ventas (idTendero,mensaje,tipoPago,valor) VALUES (%s,%s,%s,%s)",
                   (data_venta['idTendero'],data_venta['mensaje'],data_venta['tipoPago'],data_venta['valor']))
    conexion.commit()
    resultado=cursor.rowcount
    cursor.close()
    conexion.close()
    return resultado

  def insertar_costo(self,data_costo):
    conexion=obtenerConexion()
    cursor=conexion.cursor()
    cursor.execute("INSERT INTO costos (idTendero,mensaje,valor,proveedor) VALUES (%s,%s,%s,%s)",
                   (data_costo['idTendero'],data_costo['mensaje'],data_costo['valor'],data_costo['proveedor']))
    conexion.commit()
    resultado=cursor.rowcount
    cursor.close()
    conexion.close()
    return resultado

  def insertar_gasto(self,data_gasto):
    conexion=obtenerConexion()
    cursor=conexion.cursor()
    cursor.execute("INSERT INTO gastos (idTendero,mensaje,valor) VALUES (%s,%s,%s)",
                  (data_gasto['idTendero'],data_gasto['mensaje'],data_gasto['valor']))  
    conexion.commit()
    resultado=cursor.rowcount
    cursor.close()
    conexion.close()
    return resultado

  def insertarBase(self,base):
    conexion=obtenerConexion()
    cursor=conexion.cursor()
    cursor.execute("INSERT INTO apertura (idTendero, baseInicial) VALUES (%s,%s)",
                   (base["idTendero"],base["baseInicial"]))
    conexion.commit()
    resultado=cursor.rowcount
    cursor.close()
    conexion.close()
    return resultado