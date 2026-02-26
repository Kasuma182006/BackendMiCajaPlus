from conexion import obtenerConexion

class Inventario:

    def cargarInventario(self,idTendero):

        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("""Select inventario.idInventario,inventario.idProductos,inventario.cantidad,inventario.valorVenta,inventario.valorCompra, productos.idCategorias, productos.nombre, productos.presentacion FROM inventario INNER JOIN productos ON inventario.idProductos = productos.idProductos WHERE inventario.idTendero = %s """, (idTendero,))
        resultado = cursor.fetchall();
        cursor.close()
        conexion.close()
        return resultado;




