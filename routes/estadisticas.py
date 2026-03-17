from flask import request, jsonify
from models.estadisticas import Estadisticas

def cargar_rutas_estadisticas(app):

    @app.route("/consultarEstadisticas", methods=["POST"])
    def consulta_estadisticas():
        try:
            dataEstadistica = request.get_json()
            print(f"fecha estadistica {dataEstadistica}")
            estadisticasModel=Estadisticas()
            idTendero=dataEstadistica['idTendero']
            fechaInicial=dataEstadistica['fechaInicial']
            fechaFin=dataEstadistica['fechaFin']
            resultadoDatos=estadisticasModel.obtener_estadisticas(idTendero,fechaInicial,fechaFin)

            if resultadoDatos:
                print(f"resultado Estadisticas {resultadoDatos}")
            
                return jsonify([resultadoDatos]),200
            else:
                print(f"resultado bien malo {resultadoDatos}")
                return jsonify({resultadoDatos}),400
                
        
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

#     @app.route("/consultaPrimerFecha", methods=["POST"])
#     def consultar_fecha():
#         try:
#             data_primerfecha = request.get_json()
#             print(data_primerfecha)

#             fecha_model = Estadisticas()
#             datos = fecha_model.fecha_min(data_primerfecha)

#             if datos is None:
#                 datos = {"primer_fecha": None}

#             elif datos.get('primer_fecha') is not None:
#                  datos['primer_fecha'] = datos['primer_fecha'].strftime('%Y-%m-%d')

#             print(datos)
#             return jsonify(datos)
        
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500