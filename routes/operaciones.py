from flask import request,jsonify 
from models.operaciones import Operaciones

def cargar_rutas_operaciones(app):

    @app.route("/crearventas", methods=["POST"])
    def crear_venta():
        try:
            venta = request.get_json()
            venta_model = Operaciones()
            resultado=venta_model.insertar_venta(venta)

            if resultado==1:
                return jsonify({"exito": True}), 201
            
            else:
                return jsonify({"no se logro agregar"}),500

        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error interno"}), 500
        

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
        

    @app.route("/agregarBase", methods= ["POST"])
    def agregarBase():
        try:
            base = request.get_json()
            print(f"La base inicial es de {base}")
            base_model = Operaciones()
            resultado=base_model.insertarBase(base)
            if resultado==1:
                return jsonify({"exito":True}),201
            else:
                return jsonify({"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error interno"}),500
    