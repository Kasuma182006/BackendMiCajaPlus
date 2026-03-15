from conexion import obtenerConexion
from flask import request, jsonify
from models.inventario import Inventario

def cargar_rutas_inventario(app):

    @app.route("/operacionesInventario", methods=["POST"])
    def operacionesInventario():
        producto = request.get_json()
        inventario = Inventario()
        
        try:
            
            print(f"DEBUG: Buscando producto en BD: {producto.get('nombre')}")
            productoInventario = inventario.buscarProducto(producto)
            
            if not productoInventario:
                return jsonify({"error": "No se han encontrado coincidencias del producto"}), 404

            
            operacion = producto.get("operacion")
            cantidad_solicitada = producto.get("cantidad", 0)
            cantidad_actual = productoInventario.get("cantidad", 0)

            if operacion == "descontar":
                if cantidad_actual < cantidad_solicitada:
                    return jsonify({"error": "Stock insuficiente para vender"}), 400
                
                productoInventario["cantidad"] = cantidad_actual - cantidad_solicitada
                mensaje_success = "Se han descontado los productos con éxito"
                
            else: 
                productoInventario["cantidad"] = cantidad_actual + cantidad_solicitada
                mensaje_success = "Se han agregado las unidades correctamente"

            
            print(f"DEBUG: Intentando actualizar BD con nueva cantidad: {productoInventario['cantidad']}")
            inventario.actualizarUnidades(productoInventario)
            
            
            return jsonify({"status": "success", "message": mensaje_success}), 200

        except Exception as e:
            
            print(f"!!! ERROR CRÍTICO en operacionesInventario: {e}")
            return jsonify({"error": "Error interno al procesar la operación", "detalle": str(e)}), 500


    @app.route("/categorias",methods =["GET"] )
    def categorias():
        inventario= Inventario()
        try:
            print("obteniendo categorias")
            categorias = inventario.categorias()
        except Exception as e:
            print(f"Error en la consulta {e}")
            return jsonify({"Error": f"Se ha presentado un error en el servidor {e}"}),500
        return jsonify(categorias)


    @app.route("/catalogo", methods = ["GET"])
    def catalogo():
        inventario = Inventario()
        try: 
            print("obteniendo catalago")
            listaCatalogos = inventario.catalogo()
        except Exception as e:
            print(e)
            return jsonify({"Error": "Ha ocurrido un error al buscar el catalogo"}), 500
        
        return jsonify(listaCatalogos) 


    @app.route("/agregarProducto", methods = ["POST"])
    def agregarProducto():

        productoNuevo = request.get_json()
        inventario = Inventario()
        print(productoNuevo)
        try:
            verificación = inventario.buscarProducto(productoNuevo)
            if not verificación: 
                    inventario.agregarProducto(productoNuevo)
                    if productoNuevo.get("operacion") == 1: #1 significa que el tendero creo un producto sin elegir en el catalogo
                        inventario.agregarCatalogo(productoNuevo)
            else: 
                return jsonify({"Error": "El producto ya ha sido creado, elige un nombre o una presentación diferente"}),500

        except Exception as e:
                print(f"ERROR EN EL SERVIDOR, detalle : {e}")
                return jsonify({"Error": f"Ha ocurrido un error en el servidor: {e}"}), 500  
        
        return jsonify({"succesul":"El producto se ha creado con éxito"})


