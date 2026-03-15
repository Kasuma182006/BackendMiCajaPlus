from conexion import obtenerConexion

class Inventario():
    def buscarProducto(self,producto):

        conexion=obtenerConexion()
        cursor=conexion.cursor(dictionary=True)
        cursor.execute("""SELECT idInventario, cantidad FROM inventario WHERE idTendero = %s AND nombreProducto = %s AND presentacion = %s """,(producto.get("idTendero"),producto.get("nombre"),producto.get("presentacion")))
        resultado=cursor.fetchone()
        cursor.close()
        conexion.close()
        print(f"resultado de busquda = {resultado}")
        return resultado
    
    def actualizarUnidades(self,producto):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("""UPDATE inventario SET cantidad = %s where idInventario = %s """, (producto.get("cantidad"),producto.get("idInventario")))
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
