from conexion import obtenerConexion
from flask import request, jsonify
from models.inventario import Inventario


def cargar_rutas_inventario(app):

    @app.route("/operacionesInventario", methods=["POST"])
    def operacionesProductos():
        producto = request.get_json()
        inventarioTendero = Inventario()
        
        if not producto:
            return jsonify({"Error": "Datos incompletos "}),400
        else: 
            try: 
                print (producto.get("nombre")+","+producto.get("presentacion"))
                idProducto = inventarioTendero.buscarProducto( producto.get("nombre"), producto.get("presentacion"))
                productoInventario = inventarioTendero.buscarInventario(producto.get("idTendero"), idProducto.get("idProductos"))
            except Exception as e:
                print(f"error en el servidor ${e}")
                return jsonify({"error": "error, no se ha encontrado el producto"}),500
            
        if not productoInventario: 
            print("No se han encontrado coincidencias")
            return jsonify({"error": "No se ha encontrado el producto en inventario"}),404
        
        
        if (producto.get("operacion") == "descontar"):

            if productoInventario["cantidad"] >= producto["cantidad"]:
                productoInventario["cantidad"] = productoInventario["cantidad"] - producto["cantidad"]
                try:
                    inventarioTendero.actualizarProducto(productoInventario)
                    return jsonify({"succesful": "Productos descontados correctamente"}),200
                except:
                    print("error al procesar")
                    return jsonify ({"Error": "Error en al procesar"}),500
            else :  
                print("la cantidad de productos en stock es menor a la cantidad de productos vendidos")
                return jsonify({"Error": "La cantidad de productos en stok es menor a la cantidad de productos vendidos"},400)

        else: 
            productoInventario["cantidad"] = productoInventario["cantidad"] + producto["cantidad"]
            try:
                inventarioTendero.actualizarProducto(productoInventario)
                return jsonify({"succesful": "Productos agregados correctamente"}),200
            except:
                print("error al intentar agregar productos")
                return jsonify ({"Error": "Error en al intentar agregar productos"}),500
        


    @app.route("/buscarProductos", methods = ["POST"])
    def buscarProductos():
        busqueda = request.get_json()
        inventarioTendero = Inventario()
        listaInventario = []
        try:
            print(busqueda.get("nombre"))
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
                print(f"el producto {i} no está en inventario")
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
            inventarioProducto = actualizarInventario.buscarProductos(producto.get("nombre"),producto.get("presentacion"))
            print(f"Productos {inventarioProducto}")
        except Exception as e:
            print(e)
            return 500

        if not inventarioProducto:
            try:
                actualizarInventario.editarInventario(producto)
                return 200
            except Exception as e:
                print(e)
                return 500
        
        for i in inventarioProducto:
            try:
                inventarioTendero = actualizarInventario.buscarInventario(i.get("idTendero"),i.get("idProductos"))
                print(inventarioTendero)
            except Exception as e:
                print(e)
                return 500


        if not inventarioTendero:
            try: 
                actualizarInventario.editarInventario(producto)
                return jsonify({"succesful": "El Prodcuto se ha actualizado con éxito"})
            
            except Exception as e:
                print(e)
                return jsonify({"error": "Parece que ha habido un error al editar en la base de datos"})
        
        else: 

            return 409 #Codigo de error para cosas ya credas y que generan algun conflicto
            
    
    @app.route("/agregarProducto",methods = ["POST"])
    def agregarProductos():
        producto = request.get_json()
        inventarioTendero = Inventario()

        try:
            print( producto.get("categoria"))
            idCateogria = inventarioTendero.buscarCategoria(producto.get("categoria"))
                
        except Exception as e:
            print(e)
            return jsonify ({"error": "Ha habido un error al consultar la categoria"})
        
        if not idCateogria :
            return jsonify({"error":"La categoria no existe"})

        try: 
            print(producto.get("nombre"), producto.get("presentacion"))
            existencia = inventarioTendero.buscarProductos(producto.get("nombre"), producto.get("presentacion"))
            print(f"producto {existencia}")

        except Exception as e:
            print(e)
            return jsonify({"error": "Ha ocurrido un error al consultar la existencia del producto"})    

        if not existencia:
            try:

                inventarioTendero.agregarProducto(producto,idCateogria)
                return jsonify ({"succesful": "el producto se ha agregado correctamente"})

            except Exception as e:
                print(e)
                return jsonify({"error": "ha ocurrido un error al agregar el producto"})

        try : 
            for i in existencia:
                print(f"el ID del producto es {i.get('idProductos')}")
                existenciaInventario = inventarioTendero.buscarInventario(producto.get("idTendero"),i.get("idProductos"))
                print(existenciaInventario)
        except Exception as e:
            print(e)
            return jsonify({"error": "Ha ocurrido un error al buscar el producto en inventario"})
        
        if not existenciaInventario:

            inventarioTendero.agregarProducto(producto,idCateogria)
            return jsonify ({"succesful": "el producto se ha agregado correctamente"})
        else:

            return jsonify({"error": "El produco ya existe en su inventario, por favor agregue otro producto"})
        






   




                
                
        