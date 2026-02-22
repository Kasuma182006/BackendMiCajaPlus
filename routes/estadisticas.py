from flask import request, jsonify
from models.estadisticas import Estadisticas

def cargar_rutas_estadisticas(app):

    @app.route("/ConsultarEstadisticas", methods=["POST"])
    def consulta_estadisticas():
        try:
            data_estadistica = request.get_json()
            print("La referencia del reporte es:", data_estadistica)

            estadistica_model = Estadisticas()
            datos = estadistica_model.obtener_estadisticas(data_estadistica)

            
            return jsonify(datos)
        
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @app.route("/consultaPrimerFecha", methods=["POST"])
    def consultar_fecha():
        try:
            data_primerfecha = request.get_json()
            print(data_primerfecha)

            fecha_model = Estadisticas()
            datos = fecha_model.fecha_min(data_primerfecha)

            if datos is None:
                datos = {"primer_fecha": None}

            elif datos.get('primer_fecha') is not None:
                 datos['primer_fecha'] = datos['primer_fecha'].strftime('%Y-%m-%d')

            print(datos)
            return jsonify(datos)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500