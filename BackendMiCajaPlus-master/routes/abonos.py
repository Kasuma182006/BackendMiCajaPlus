from flask import request,jsonify
from models.abonos import Abonos
from models.clientes import Clientes

def cargar_ruta_abonos(app):

    @app.route("/abonos", methods=["POST"])
    def aplicar_abonos():
        try:
            datos=request.get_json()
            print(f"datos abono {datos}")
            cedulaCliente=datos['cedula']
            cedulaTendero=datos['idTendero']
            montoAbonar=datos['abono']
            clienteModel=Clientes()
            cliente=clienteModel.ConsultarClientes(datos)
            if cliente:
                idCliente=cliente['idCliente']
                saldoActual = cliente['saldo']
                nuevoSaldo = saldoActual - montoAbonar
                if nuevoSaldo >= 0:
                    abonoModel = Abonos()
                    resultadoAbono = abonoModel.aplicar_abono(datos, idCliente)
                
                    if resultadoAbono > 0:
                        clienteModel.actualizarSaldo(datos['cedula'], datos['idTendero'], nuevoSaldo)
                        return jsonify({"mensaje": "Abono exitoso", "nuevoSaldo": nuevoSaldo}), 201
                    else:
                        return jsonify({"error": "No se pudo registrar el abono en la tabla"}), 500
                else:
                    return jsonify({
                        "error": "Monto excedido", 
                        "mensaje": f"El cliente solo debe {saldoActual}. No puedes abonar {montoAbonar}."}), 400
            else:
                return jsonify({"error": "Cliente no encontrado"}), 404

        except Exception as e:
            print(f"error abono {e}")
            return jsonify ({"error": str(e)})
                