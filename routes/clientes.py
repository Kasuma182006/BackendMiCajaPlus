from flask import request,jsonify 
from models.clientes import Clientes

def cargar_rutas_clientes(app):

    
    @app.route("/")
    def index():
        return "micaja+"


    @app.route("/consultarcliente", methods=["GET"])
    def consultar_cliente():
        try:
            cedula = request.args.get("cedula")
            if not cedula:
                return jsonify({"error": "Falta la cédula"}), 400

            cliente_model = Clientes()
            resultado = cliente_model.ConsultarClientes(cedula)

            print("Resultado SQL:", resultado)  # imprime lo que devuelve la consulta

            if resultado:
                return jsonify({"registrado": True}), 200
            else:
                return jsonify({"registrado": False}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @app.route("/agregarcliente", methods=["POST"])
    def agregar_cliente():
        try:
            data_cliente=request.get_json()
            print("datos resividos", data_cliente)
            cliente_model=Clientes()
            cliente_model.insertar_cliente(data_cliente)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"error": str(e)})
