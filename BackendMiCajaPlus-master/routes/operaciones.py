from flask import request,jsonify 
from models.operaciones import Operaciones
from models.clientes import Clientes
from models.creditos import Creditos
from models.inventario import Inventario

def cargar_rutas_operaciones(app):
    
    # probar si sirve

    @app.route("/crearventas", methods=["POST"])
    def crear_venta():
        try:
            venta = request.get_json()
            print(f"datos Venta {venta}")
            
            inventarioModel = Inventario()
            resultado = inventarioModel.obtenerPrecio(venta)

            if not resultado:
                return jsonify({"error": "Producto no encontrado"}), 404
           
            precioUnitario = resultado["valorVenta"]
            cantidad = venta.get('cantidad', 1)
            venta['valor'] = precioUnitario * cantidad
            tipoPago = venta.get('tipoPago')

            tipoPago=venta['tipoPago']
            
            if tipoPago == "credito":
                    ventaModel = Operaciones()
                    cliente = Clientes()
                    resultadoCliente = cliente.ConsultarClientes(venta)
                    resultadoVenta=ventaModel.insertar_venta(venta)
                    if resultadoVenta > 0:
                        print("entro a resultadoVenta")
                        print(f"DEBUG: tipo de resultadoVenta es {type(resultadoVenta)} y su valor es {resultadoVenta}")
                        idVenta= resultadoVenta
                        idCliente= resultadoCliente["idCliente"]
                        creditoModel= Creditos()
                        resultadoCredito=creditoModel.insertar_credito(idVenta,idCliente)
                        if resultadoCredito > 0:
                            insertar_credito = creditoModel.aumentar_saldo(venta, idCliente)
                            if(insertar_credito == True):
                                return jsonify({"exitoso":"credito exitoso"}),201
                            else:
                                return jsonify({"exito":"ocurrio un problema en el credito"}),500
                            
                    else:
                        return jsonify({"exito":"no se pudo registrar la venta"}),500   
            else:
                ventaModel = Operaciones()
                resultadoVenta=ventaModel.insertar_venta(venta)
                if resultadoVenta > 0:
                    return jsonify ({"exito": True, "total": venta['valor']}),201
                
                else:
                    return jsonify({"error": "error venta"}),500
                       
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error": "error interno"}), 500
        

    @app.route("/crearcosto", methods=["POST"])
    def crear_costo():
        try:
            costo=request.get_json()
            costo_model=Operaciones()
            resultado=costo_model.insertar_costo(costo)

            if resultado==1:
                return jsonify({"exito": True}),201
            else:
                return jsonify({"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error interno"}),500
        
    @app.route("/creargasto", methods=["POST"])    
    def crear_gasto():
        try:
            gasto=request.get_json()
            gasto_model=Operaciones()
            resultado=gasto_model.insertar_gasto(gasto)

            if resultado==1:
                return jsonify({"exito":True}),201
            else:
                return jsonify({"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error interno"}),500
        
    
    @app.route("/cantidadProducto", methods= ["POST"])
    def cantidadProducto():
        try:
            conexion = request.get_json()
            modelCantidad= Inventario()
            print(conexion)
            cantidad = conexion.get('cantidad')
            resultado = modelCantidad.obtenerPrecio(conexion)
            precioUnitario = resultado['cantidad']
            
            if precioUnitario >= cantidad:
                return jsonify({"exito": True}),200
            else:
                return jsonify({"error": False}),500
            
        except Exception as e:
            return jsonify({"Error": e}),500
        

    @app.route("/agregarBase", methods= ["POST"])
    def agregarBase():
        try:
            base = request.get_json()
            print(f"La base inicial es de {base}")
            base_model = Operaciones()
            resultado=base_model.insertarBase(base)
            if resultado > 0:
                return jsonify({"exito":True}),201
            else:
                return jsonify({"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error interno"}),500
    