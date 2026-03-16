from conexion import obtenerConexion

class Inventario():
    def buscarProducto(self,idTendero,nombre,presentacion):

        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("""SELECT idInventario, cantidad,valorCompra FROM inventario WHERE idTendero = %s AND nombreProducto = %s AND presentacion = %s """,(idTendero,nombre,presentacion))
        resultado=cursor.fetchone()
        cursor.close()
        conexion.close()
        print(f"resultado de busquda = {resultado}")
        return resultado
    
    def actualizarUnidades(self,producto,operacion):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        print(operacion)
        if operacion == "descontar":
            cursor.execute("""UPDATE inventario SET cantidad = %s where idInventario = %s """, (producto.get("cantidad"),producto.get("idInventario")))
        else:
            print(producto.get("valorCompra"))
            cursor.execute("""UPDATE inventario SET cantidad = %s, valorCompra = %s where idInventario = %s """, (producto.get("cantidad"),producto.get("valorCompra"),producto.get("idInventario")))
        conexion.commit()
        cursor.close()
        conexion.close()
    
    def catalogo(self):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("Select idCategorias, nombre, presentacion from productos")
        resultado=cursor.fetchall()
        cursor.close()
        conexion.close()
        print(f"resultado de busquda = {resultado}")
        return resultado
    
    def categorias(self):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("Select idCategorias, nombre from categorias")
        resultado=cursor.fetchall()
        cursor.close()
        conexion.close()
        print(f"resultado de busquda = {resultado}")
        return resultado                                              

    def agregarProducto(self,producto):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO inventario(idTendero,cantidad,valorVenta,valorCompra,nombreProducto,presentacion,nombreCategoria) VALUES(%s,%s,%s,%s,%s,%s,%s)""",(producto.get("idTendero"),producto.get("cantidad"),producto.get("valorVenta"),producto.get("valorCompra"),producto.get("nombre"),producto.get("presentacion"),producto.get("idCategoria")))
        conexion.commit()
        cursor.close()
        conexion.close()


    def agregarCatalogo(self,catalogo):

        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""INSERT INTO productos(nombre,presentacion,idCategorias) VALUES(%s,%s,%s)""",(catalogo.get("nombre"), catalogo.get("presentacion"),catalogo.get("idCategoria")))
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtenerPrecio(self,producto):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        try:
    
            cursor.execute( """
                SELECT valorVenta,cantidad
                FROM inventario 
                WHERE idTendero = %s  AND nombreProducto = %s AND presentacion = %s
            """, (producto["idTendero"], producto["nombre"], producto["presentacion"])), 

        
            resultado= cursor.fetchone()
            return resultado 
        finally:    
            cursor.close()
            conexion.close()

    def sugerirProductos(self,producto):
        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        nombre = f"%{producto.get("nombre")}%"
        cursor.execute("""Select idInventario,nombreProducto,presentacion,cantidad,valorVenta,valorCompra from inventario where idTendero = %s AND nombreProducto LIKE %s""",(producto.get("idTendero"),nombre))
        resultado=cursor.fetchall()
        cursor.close()
        conexion.close()
        print(f"resultado de busquda = {resultado}")
        return resultado


    def editarProducto(self,producto):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""UPDATE inventario SET cantidad = %s,valorVenta = %s ,valorCompra = %s ,nombreProducto = %s ,presentacion = %s ,nombreCategoria = %s WHERE idInventario = %s""" ,(producto.get("cantidad"),producto.get("valorVenta"),producto.get("valorCompra"),producto.get("nombreProducto"),producto.get("presentacion"),producto.get("nombreCategoria"),producto.get("idInventario")))
        conexion.commit()
        cursor.close()
        conexion.close()