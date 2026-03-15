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
            resultadoInv = inventarioModel.obtenerPrecio(venta)
            if resultadoInv:
                precioUnitario = resultadoInv['valorVenta']
                cantidad = venta['cantidad']
                venta['valor'] = precioUnitario * cantidad
                tipoPago=venta['tipoPago']
                if cantidad > 0:                
                    if tipoPago == "credito":
                        cedulaCliente=venta['cedulaCliente']
                        cedulaTendero=venta['idTendero']
                        clienteModel=Clientes()
                        resultadoCliente=clienteModel.ConsultarClientes(cedulaCliente,cedulaTendero)
                        if resultadoCliente:
                            ventaModel = Operaciones()
                            resultadoVenta=ventaModel.insertar_venta(venta)
                            if resultadoVenta > 0:
                                idVenta=resultadoVenta['idVenta']
                                idCliente=resultadoCliente['idCliente']
                                creditoModel= Creditos()
                                resultadoCredito=creditoModel.insertar_credito(idVenta,idCliente)
                                if resultadoCredito > 0:
                                    return jsonify({"exitoso":"credito exitoso"}),201
                                else:
                                    return jsonify({"exito":"ocurrio un problema en el credito"}),400
                            else:
                                return jsonify({"exito":"no se pudo registrar la venta"}),400
                        else:
                            return jsonify({"exito":"cliente no registrado"}),400
                    else:
                        ventaModel = Operaciones()
                        resultadoVenta=ventaModel.insertar_venta(venta)
                        if resultadoVenta > 0:
                            return jsonify ({"exito": True, "total": venta['valor']}),201
                        
                        else:
                            return jsonify({"error": "error venta"}),500
                else:
                    return jsonify({"error":"no hay stock"}),404   
            else:
                return jsonify({"error":"fallo inventario"}) ,400        
                            
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
                return jsonify({"error":"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error":"error interno"}),500
        

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
            
    @app.route("/cantidadProducto", methods= ["POST"])
    def cantidadProducto():
        try:
            conexion = request.get_json()
            modelCantidad= Inventario()
            cantidad = conexion.get('cantidad')
            resultado = modelCantidad.obtenerPrecio(conexion)
            precioUnitario = resultado['cantidad']
            
            if precioUnitario >= cantidad:
                return jsonify({"exito": True}),200
            else:
                return jsonify({"error": False}),500
            
        except Exception as e:
            return jsonify({"Error": e}),500    

        