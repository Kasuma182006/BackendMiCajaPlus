from conexion import obtenerConexion
from flask import request, jsonify
from models.inventario import Inventario


def cargar_rutas_inventario(app):

    @app.route("/descargaProductos", methods=["POST"])
    def operacionesProductos():
        producto = request.get_json()
        inventarioTendero = Inventario()
        
        if not producto:
            return jsonify({"Error": "Datos incompletos "}), 400
        else: 
            try: 
                idProducto = inventarioTendero.buscarProducto( producto.get("nombre"), producto.get("presentacion"))
                productoInventario = inventarioTendero.buscarInventario(producto.get("idTendero"), idProducto.get("idProductos"))
            except:
                return jsonify({"error": "error en el servidor"}),500
            
        if not productoInventario: 
            return jsonify({"error" "No se ha encontrado el producto en inventario"})

        if productoInventario["cantidad"] >= producto["cantidad"]:
           productoInventario["cantidad"] = productoInventario["cantidad"] - producto["cantidad"]
           try:
                inventarioTendero.actualizarProducto(productoInventario)
                return jsonify({"succesful": "Productos descontados correctamente"}),200
           except:
               return jsonify ({"Error": "Error en al procesar"}),500
        else :  
            return jsonify({"Error": "La cantidad de productos en stok es menor a la cantidad de productos vendidos"})          