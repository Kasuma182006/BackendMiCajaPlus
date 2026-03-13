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
    

    def buscarProductosSimilares(self,nombre):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary= True)
        patron = f"%{nombre}%"
        cursor.execute("""Select idProductos FROM productos where nombre like %s """,(patron,))
        resultado= cursor.fetchall()
        cursor.close()
        conexion.close()
        print(resultado)
        return resultado
    
    def buscarProductos(self,nombre,presentacion):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary= True)
        cursor.execute("""Select idProductos FROM productos where nombre = %s and presentacion = %s """,(nombre,presentacion,))
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

    def obtenerPrecio(self,Producto):
        conexion = obtenerConexion()
        cursor = conexion.cursor()
        try:
    
            cursor.execute( """
                SELECT i.valorVenta, p.nombre 
                FROM inventario i
                INNER JOIN productos p ON i.idProductos = p.idProductos 
                WHERE i.idTendero = %s AND p.nombre = %s
            """, (Producto["idTendero"], Producto["nombre"]))

            resultado= cursor.fetchone()
            return resultado 
        finally:    
            cursor.close()
            conexion.close()
        

    def buscarCategoria(self, categoria):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary= True)
        cursor.execute("""Select idCategorias FROM categorias where nombre = %s """,(categoria,))
        resultado= cursor.fetchone()
        cursor.close()
        conexion.close()
        print(resultado)
        return resultado
    
    def agregarProducto(self,producto,idCategoria):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO productos(idCategorias,nombre,presentacion) VALUES(%s,%s,%s) """,(idCategoria.get("idCategorias"),
                                                                                                                producto.get("nombre"),
                                                                                                                producto.get("presentacion"),)
        )
        conexion.commit()
        idProducto = cursor.lastrowid
        cursor.execute("""INSERT INTO inventario(idTendero,idProductos,cantidad,valorVenta,ValorCompra) VALUES(%s,%s,%s,%s,%s) """,(producto.get("idTendero"),idProducto,0,0,0 ))
        conexion.commit()
        cursor.close()
        conexion.close()
        





