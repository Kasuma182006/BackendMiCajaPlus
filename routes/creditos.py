
from flask import request,jsonify 
from models.creditos import Creditos
from conexion import obtenerConexion

def cargar_rutas_credito(app):

    @app.route("/consultarCreditos", methods=["GET"])
    def consultaCreditosVisualizar():
        try:
            idtendero = request.args.get("idTendero")
            print("el idTendero es ",idtendero)
            creditos_model = Creditos()
            datos = creditos_model.consultar_creditos(idtendero)
            return jsonify(datos)
        except Exception as e:
            return jsonify({"error": str(e)})
       
        
    @app.route("/AgregarCredito", methods=["POST"])
    def agregar_credito():
        try:
            data_credito=request.get_json()
            print("datos resividos",data_credito)
            creditos_model=Creditos()
            creditos_model.insertar_credito(data_credito)
            return jsonify({"success":True})
        except Exception as e:
            return jsonify({"error": str(e)})
        
    @app.route("/buscar_cliente", methods =['POST'])
    def buscar():
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        data = request.get_json()
        identificacion = data['cedula']
        tendero = data['tendero']
        sql = "SELECT cedula, nombre, telefono, count(id_credito) as creditos, sum(valor) as total FROM clientes LEFT JOIN creditos on cedula = id_cliente AND creditos.activo = 1 AND creditos.id_tendero =%s WHERE cedula=%s GROUP BY cedula, nombre, telefono"
        cursor.execute(sql,(tendero, identificacion,))
        resultado = cursor.fetchone()
        print(resultado)
        if resultado:
            cliente = {
            "cedula": resultado["cedula"],
            "nombre": resultado["nombre"],
            "celular": resultado["telefono"],
            "creditos": resultado["creditos"],
            "total": resultado["total"] if resultado["total"] is not None else 0
}
            return jsonify([cliente])
        return jsonify([])

    @app.route("/insertarcliente_credito", methods =['POST'])    
    def insertar_cliente():
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        data = request.get_json()
        print(f"los datos insert cliente son ",data)
        cedulaCliente = data['cedulaCliente']
        cedulaTendero = data['cedulaTendero']
        nombre = data['nombre']
        celular = data['celular']
        monto = data['monto']
        sql = "INSERT INTO clientes(cedula,idTendero,nombre,telefono) values (%s,%s,%s,%s) "
        cursor.execute(sql,(cedulaCliente,cedulaTendero,nombre,celular))
        sql = "INSERT INTO operaciones (tipo,valor,idCliente,tipoPago,idTendero) values('venta',%s,%s,1,%s)"
        cursor.execute(sql,(monto,cedulaCliente,cedulaTendero))
        id_venta = cursor.lastrowid
        sql = "INSERT INTO creditos (id_venta,id_cliente,id_tendero,valor,activo) values(%s,%s,%s,%s,1)"
        cursor.execute(sql,(id_venta,cedulaCliente,cedulaTendero,monto))
        conexion.commit()
        return jsonify({"success": True})

    @app.route("/insertar_credito", methods = ['POST'])
    def insertar_credito():
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        data = request.get_json()
        cedulaCliente = data['cedulaCliente']
        cedulaTendero = data['cedulaTendero']
        monto = data['monto']
        sql = "INSERT INTO operaciones (tipo,valor,idCliente,tipoPago,idTendero) values('venta',%s,%s,1,%s)"
        cursor.execute(sql,(monto,cedulaCliente,cedulaTendero))
        id_venta = cursor.lastrowid
        sql = "INSERT INTO creditos (id_venta,id_cliente,id_tendero,valor,activo) values(%s,%s,%s,%s,1)"
        cursor.execute(sql,(id_venta,cedulaCliente,cedulaTendero,monto))
        conexion.commit()
        return jsonify({"success": True})

    @app.route("/abono", methods=['PUT'])
    def abono():
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        data = request.get_json()
        id_cliente = data['cedulaCliente']
        id_tendero = data['cedulaTendero']
        monto_abono = data['monto']

        sql = """
        SELECT id_credito, valor 
        FROM creditos
        WHERE id_cliente = %s AND activo = 1 AND id_tendero = %s
        ORDER BY fecha ASC
        """
        cursor.execute(sql, (id_cliente, id_tendero))
        resultado = cursor.fetchall()

        restante = monto_abono

        for credito in resultado:
            id_credito = credito["id_credito"]
            valor_credito = credito["valor"]

            if restante <= 0:
                break

            if restante >= valor_credito:
                # El abono cubre todo → dejar en 0 y desactivar
                sql = "UPDATE creditos SET valor = 0, activo = 0 WHERE id_credito = %s"
                cursor.execute(sql, (id_credito,))
                restante -= valor_credito
                conexion.commit()
            else:
                # Abono parcial
                nuevo_valor = valor_credito - restante
                sql = "UPDATE creditos SET valor = %s WHERE id_credito = %s"
                cursor.execute(sql, (nuevo_valor, id_credito))
                restante = 0
                conexion.commit()

        return jsonify({"success": True})

    @app.route("/numerocredito", methods=["POST"])
    def numerocredito():
        try:
            datos_credito = request.get_json()
            print("La referencia del reporte es:", datos_credito)

            credito_model = Creditos()
            datos = credito_model.contar_creditos(datos_credito)
            print("hola peluche",datos)
            return jsonify(datos)
        except Exception as e:
            return jsonify({"error": str(e)}), 500