from conexion import obtenerConexion
from flask import request, jsonify
from models.inventario import Inventario


def cargar_rutas_inventario(app):

    @app.route("/operacionesProductos", methods=["POST"])
    def operacionesProductos():
        try:
            idTendero = request.args.get("idTendero")
            inventario = Inventario()
            datosInventario = inventario.cargarInventario(idTendero)
            return jsonify(datosInventario);
        except Exception as e:
            return jsonify({"error": str(e)})