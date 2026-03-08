from conexion import obtenerConexion

class Abonos:

    def aplicar_abono(self,abono,idCliente):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("INSERT INTO abonos(idTendero,idCliente,abono) VALUES (%s,%s,%s)",
        (abono['idTendero'],idCliente,abono['abono']))
        conexion.commit()
        resultado=cursor.rowcount
        cursor.close()
        conexion.close()
        return resultado
    