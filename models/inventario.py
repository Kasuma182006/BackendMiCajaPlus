from conexion import obtenerConexion

class Inventario:

    def buscarProducto(self,nombre,presentacion):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary= True)
        cursor.execute("""Select idProductos FROM productos where nombre = %s AND presentacion = %s""",(nombre,presentacion))
        resultado= cursor.fetchone()
        cursor.close()
        conexion.close()
        print(resultado)
        return resultado
   
    def buscarInventario(self,idTendero,idProducto):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("""Select idInventario, cantidad From inventario where idTendero = %s AND idProductos = %s""", (idTendero,idProducto) )
        resultado= cursor.fetchone()
        cursor.close()
        conexion.close()
        print(resultado)
        return resultado
        
    

    def actualizarProducto(self, producto):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""UPDATE inventario SET cantidad = %s where idInventario = %s""",(producto["cantidad"], producto["idInventario"]) )
        conexion.commit()
        cursor.close()
        conexion.close()
    









