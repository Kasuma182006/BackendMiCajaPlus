from flask import session, jsonify

def cargar_rutas_sesion(app):

    @app.route("/sesion", methods=["GET"])
    def obtener_sesion():
        try:
            # Verificamos si la clave 'cedula' existe en la sesión del servidor
            if 'cedula' in session:
                return jsonify({
                    "logueado": True,
                    "cedula": session.get('cedula'),
                    "nombre": session.get('nombre')
                }), 200

            # Si no existe, devolvemos un 401 (No autorizado)
            return jsonify({
                "logueado": False,
                "mensaje": "No hay sesión activa"
            }), 401

        except Exception as e:
            print(f"Error en ruta /sesion: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/logout", methods=["POST"])
    def cerrar_sesion():
        """Ruta extra para limpiar la sesión del servidor"""
        session.clear()
        return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200