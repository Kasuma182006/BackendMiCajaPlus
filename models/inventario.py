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
    

    def buscarProductosSimilares(self,nombre):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary= True)
        cursor.execute("""Select idProductos FROM productos where nombre = %s """,(nombre,))
        resultado= cursor.fetchall()
        cursor.close()
        conexion.close()
        print(resultado)
        return resultado


    def productosInventario(self,idProducto,idTendero):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("""Select inventario.idInventario,productos.idProductos, inventario.cantidad, inventario.valorVenta, productos.nombre, productos.presentacion From inventario INNER JOIN productos on inventario.idProductos = productos.idProductos where inventario.idTendero = %s AND inventario.idProductos =%s """, (idTendero,idProducto))
        resultado= cursor.fetchone()
        cursor.close()
        conexion.close()
        print(f" en el inventario hay ${resultado}")
        return resultado

    
    def editarInventario(self,producto):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""UPDATE inventario SET cantidad = %s, valorVenta = %s where idInventario = %s""",(producto["cantidad"],producto["valorVenta"],producto["idInventario"],) )
        conexion.commit()
        cursor.execute("""UPDATE productos SET nombre = %s, presentacion = %s  where idProductos = %s""",( producto["nombre"],producto["presentacion"], producto["idProductos"],))
        conexion.commit()
        cursor.close()
        conexion.close()
    





