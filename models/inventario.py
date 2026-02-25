from conexion import obtenerConexion

class Inventario:

    def cargarInventario(self,idTendero):

        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""Select * FROM inventario INNER JOIN productos ON inventario.idProductos = productos.idProductos WHERE inventario.idTendero = %s """, (idTendero,))
        resultado = cursor.fetchall();
        cursor.close()
        conexion.close()
        return resultado;




