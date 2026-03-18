from flask import request, jsonify
from datetime import datetime
from models.estadisticas import Estadisticas

def cargar_rutas_estadisticas(app):

    @app.route("/consultarEstadisticas", methods=["POST"])
    def consulta_estadisticas():
        try:
            dataEstadistica = request.get_json()
            print(f"datos recibidos {dataEstadistica}")

            estadisticasModel = Estadisticas()

            idTendero = dataEstadistica['idTendero']

            # Fecha actual calculada en el backend
            hoy = datetime.now().strftime('%Y-%m-%d')

            fechaInicial = hoy
            fechaFin = hoy

            resultadoDatos = estadisticasModel.obtener_estadisticas(
                idTendero,
                fechaInicial,
                fechaFin
            )

            print(f"resultado Estadisticas {resultadoDatos}")

            return jsonify(resultadoDatos)

        except Exception as e:
            print("Error en consultarEstadisticas:", e)
            return jsonify({"error": str(e)}), 500
        
        
    @app.route("/historialActividades", methods=["POST"])
    def historial_actividades():

        data = request.get_json()

        idTendero = data["idTendero"]
        fechaInicial = data.get("fechaInicial")
        fechaFin = data.get("fechaFin")

        # Si no vienen fechas, usar hoy
        if not fechaInicial or not fechaFin:
            hoy = datetime.now().strftime('%Y-%m-%d')
            fechaInicial = hoy
            fechaFin = hoy

        modelo = Estadisticas()
        resultado = modelo.obtener_historial(idTendero, fechaInicial, fechaFin)

        return jsonify(resultado)
    
    @app.route("/reportePorRango", methods=["POST"])
    def reporte_por_rango():
        try:
            data = request.get_json()
            id_tendero = data.get('idTendero')
            fecha_inicio = data.get('fechaInicio')
            fecha_fin = data.get('fechaFin')

            modelo = Estadisticas()
            datos = modelo.obtener_reporte_rango(id_tendero, fecha_inicio, fecha_fin)

            # --- CORRECCIÓN DE CODEXXO: Convertir None a 0 ---
            # Usamos 'or 0' para que si el valor es None o False, se convierta en 0.
            ventas = datos.get('total_ventas') or 0
            costos = datos.get('total_costos') or 0
            gastos = datos.get('total_gastos') or 0
            
            # Calculamos la utilidad de forma segura
            utilidad = ventas - (costos + gastos)
            
            # Actualizamos el diccionario con los valores limpios
            datos['total_ventas'] = ventas
            datos['total_costos'] = costos
            datos['total_gastos'] = gastos
            datos['utilidad'] = utilidad

            return jsonify(datos)
        except Exception as e:
            # Esto te ayudará a ver el error real en la terminal de VS Code
            print(f"Error en reportePorRango: {e}") 
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