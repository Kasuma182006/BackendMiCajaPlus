from flask import request, jsonify
from models.tenderos import Tenderos
from argon2 import PasswordHasher

hp=PasswordHasher(hash_len=32)

def cargar_rutas_Tenderos(app):

    @app.route("/addtendero", methods=["POST"])
    def crear_tendero():
        try:
            data = request.get_json()
            print("Datos recibidos:", data)
            cedula = data["cedula"]
            telefono = data["telefono"]
            nombre = data["nombre"]

            hash_telefono=hp.hash(telefono)

            if not cedula or not telefono or not nombre:
                return jsonify({"error": "Faltan datos"}), 400

            tendero_model = Tenderos()
            resultado=tendero_model.crear_tendero(cedula,hash_telefono,nombre)
            if resultado==1:
                return jsonify({"mensaje": "Tendero creado"}), 201
            else:
                return jsonify({"error":"Error al crear"}),500

        except Exception as e:
            print("Error al crear tendero:", e)
            return jsonify({"error"}), 500


    @app.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()
            print("Datos recibidos en login:", data)
            cedula = data.get("cedula")
            telefono = data.get("telefono")

            if not cedula or not telefono:
                return jsonify({"error": "Faltan datos"}), 400

            tendero_model = Tenderos()
            usuario = tendero_model.validar_login(cedula)
            print(f"datos recibidos consulta",usuario)
            if not usuario:
                return jsonify({"error": "Credenciales incorrectas"}), 401
            try:
                hp.verify(usuario["llave"], telefono)
            except:
                return jsonify({"error":"Credenciales incorrectas"}), 401

            return jsonify(usuario), 200

        except Exception as e:
            print("Error en login:", e)
            return jsonify({"error"}), 500