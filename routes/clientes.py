from flask import request,jsonify 
from models.clientes import Clientes

def cargar_rutas_clientes(app):

    @app.route("/consultarcliente", methods=["POST"])
    def consultar_cliente():
        try:
            datosCliente=request.get_json()
            print(datosCliente)
            cliente_model = Clientes()
            resultado = cliente_model.ConsultarClientes(datosCliente)
            print(f"Resultado de la BD: {resultado}")
            if resultado: 
                return jsonify(resultado), 200
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500

#editar cliente en routes   
    @app.route("/actualizar_cliente", methods=["POST"])
    def actualizar():
        datos = request.get_json()
        model = Clientes()
        if model.actualizar_cliente(datos):
            return jsonify({"mensaje": "exito"}), 200
        return jsonify({"mensaje": "error"}), 400
        

#     @app.route("/agregarcliente", methods=["POST"])
#     def agregar_cliente():
#         try:
#             data_cliente=request.get_json()
#             print("datos resividos", data_cliente)
#             cliente_model=Clientes()
#             cliente_model.insertar_cliente(data_cliente)
#             return jsonify({"success": True})
#         except Exception as e:
#             return jsonify({"error": str(e)})
