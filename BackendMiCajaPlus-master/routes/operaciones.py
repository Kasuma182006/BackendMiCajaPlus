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
        

    @app.route("/registrar_credito", methods = ['POST'])

    def registrar_credito():

        try:

            data = request.get_json()

            print(data)

            nombre = data['nombre']

            presentacion = data['presentacion']

            cantidad = data['cantidad']

            cedulaTendero = data['idTendero']

            cedulaCliente = data['cedula']

            mensaje = data["mensaje"]

            inventario = Inventario()

            sinonimo = inventario.buscarSinonimoProducto(data)

            if sinonimo :

                nombre = sinonimo["nombre"]

            producto_inventario = inventario.buscarProducto(cedulaTendero,nombre,presentacion)


            if producto_inventario:

                cantidad_stock = producto_inventario["cantidad"]

                if cantidad > cantidad_stock:

                    return jsonify("La cantidad de venta es mayor a la cantidad en stock. Por favor actualice el inventario.")

                else:

                    cantidad_total = cantidad_stock - cantidad

                    producto = {"cantidad": cantidad_total, "idInventario": producto_inventario["idInventario"]}

                    inventario.actualizarUnidades(producto, "descontar")

                    data["valor"] = producto_inventario["valorVenta"] * cantidad  

                    operacion = Operaciones()

                    venta = operacion.insertar_venta(data)

                    if venta:

                        creditoModel= Creditos()

                        cliente = Clientes()

                        resultado_cliente = cliente.ConsultarClientes(data)

                        idCliente = int(resultado_cliente["idCliente"])

                        creditoModel.insertar_credito(int(venta), int(idCliente))

                        saldo = creditoModel.aumentar_saldo(data,idCliente)

                        if saldo == True:

                            return jsonify("La venta a crédito ha sido registrado con éxito. ¿Algo más? para finalizar di fin.")

                        else:

                            return jsonify("Ha ocurrido un error. Intentelo de nuevo.")

                    else:

                        return jsonify("Ha ocurrido un error a la hora de registrar la venta por favor intentelo de nuevo.")

            else:

                return jsonify("El producto no esta registrado. Por favor agregalo al inventario. Para finalizar el crédito di fin.")

        except Exception as e:

                    print(f"Error detectado: {e}")

                    return jsonify({"Error interno": e})
        

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
    