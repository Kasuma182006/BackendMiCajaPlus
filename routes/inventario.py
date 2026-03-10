from conexion import obtenerConexion
from flask import request, jsonify
from models.inventario import Inventario


def cargar_rutas_inventario(app):

    @app.route("/operacionesInventario", methods=["POST"])
    def operacionesProductos():
        producto = request.get_json()
        inventarioTendero = Inventario()
        
        if not producto:
            return jsonify({"Error": "Datos incompletos "})
        else: 
            try: 
                idProducto = inventarioTendero.buscarProducto( producto.get("nombre"), producto.get("presentacion"))
                productoInventario = inventarioTendero.buscarInventario(producto.get("idTendero"), idProducto.get("idProductos"))
            except:
                return jsonify({"error": "error en el servidor"})
            
        if not productoInventario: 
            return jsonify({"error" "No se ha encontrado el producto en inventario"})
        
        if (producto.get("operacion") == "descontar"):

            if productoInventario["cantidad"] >= producto["cantidad"]:
                productoInventario["cantidad"] = productoInventario["cantidad"] - producto["cantidad"]
                try:
                    inventarioTendero.actualizarProducto(productoInventario)
                    return jsonify({"succesful": "Productos descontados correctamente"})
                except:
                    return jsonify ({"Error": "Error en al procesar"})
            else :  
                return jsonify({"Error": "La cantidad de productos en stok es menor a la cantidad de productos vendidos"},400)

        else: 
            productoInventario["cantidad"] = productoInventario["cantidad"] + producto["cantidad"]
            try:
                inventarioTendero.actualizarProducto(productoInventario)
                return jsonify({"succesful": "Productos agregados correctamente"})
            except:
                return jsonify ({"Error": "Error en al intentar agregar productos"})
        


    @app.route("/buscarProductos", methods = ["POST"])
    def buscarProductos():
        busqueda = request.get_json()
        inventarioTendero = Inventario()
        listaInventario = []
        try:
            listaProductos =  inventarioTendero.buscarProductosSimilares(busqueda.get("nombre"))
        except Exception as e:
            print(e)
            return jsonify({"error": "error con el servidor"})
            
        
        if not listaProductos:
            return jsonify({"error": "No se han encontrado coincidencias en los productos"})
        
        print(f"lista de productos ${listaProductos}")
        
        for i in listaProductos:
            
            try:
                print(i.get("idProductos"),busqueda.get("idTendero"))
                producto = (inventarioTendero.productosInventario(i.get("idProductos"),busqueda.get("idTendero")))
                print(f"el producto es ${producto}")
            except Exception as e:
                print(e)
                return jsonify({"error":"error al consultar en la base de datos"})
            if not producto:
                print(f"el producto ${i} no está en inventario")
                producto = ""
            else: 
                listaInventario.append(producto)
                producto = ""
        
        print(f" hay ${listaInventario} productos en inventario" )
        
        if not listaInventario: 
            return jsonify({"error": "El producto no se encuentra en su inventario"})
        
        else: 
            return jsonify (listaInventario)

    @app.route("/editarProducto", methods = ["POST"])
    def editarProductos():
        producto = request.get_json()
        actualizarInventario = Inventario()
        try: 
            actualizarInventario.editarInventario(producto)
            return jsonify({"succesful": "El Prodcuto se ha actualizado con éxito"})
        
        except Exception as e:
            print(e)
            return jsonify({"error": "Parece que ha habido un error al editar en la base de datos"})


   




                
                
        