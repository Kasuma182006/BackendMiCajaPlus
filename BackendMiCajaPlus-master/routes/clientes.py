from flask import request,jsonify 
from models.clientes import Clientes
from conexion import obtenerConexion

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
    
    @app.route("/registrar_venta", methods = ['POST'])
    def registrar_venta():
        try:
            conexion = obtenerConexion()
            cursor = conexion.cursor(dictionary=True)
            data = request.get_json()
            nombre = data['nombreProducto']
            presentacion = data['presentacion']
            cantidad = data['cantidad']
            cedulaTendero = data['idTendero']
            cedulaCliente = data['idcliente']
          
            print(data)
            sql = """SELECT p.idProductos, i.valorVenta FROM diccionarioproductos d JOIN productos p ON d.idProductos = p.idProductos JOIN inventario i ON p.idProductos = i.idProductos WHERE d.sinonimo = %s AND p.presentacion = %s AND i.cantidad >= %s;"""
            cursor.execute(sql,(nombre,presentacion, cantidad,))
            resultado = cursor.fetchone()
            print(resultado)
            if resultado:
                    productos = resultado["idProductos"]
                    sql = """UPDATE inventario SET cantidad = cantidad - %s WHERE idProductos = %s AND idTendero = %s;"""
                    cursor.execute(sql,(cantidad,productos,cedulaTendero,))
                    conexion.commit()
                    mensaje = nombre + presentacion + str(cantidad)
                    valor = resultado["valorVenta"] * cantidad
                    sql ="""INSERT INTO ventas (idTendero, mensaje, tipoPago, valor) VALUES (%s, %s, %s, %s);"""
                    cursor.execute(sql,(cedulaTendero,mensaje,"credito",valor,))
                    conexion.commit()
                    idVenta = cursor.lastrowid
                    print(data)
                    sql = """SELECT idCliente FROM cliente WHERE cedula = %s AND idTendero = %s"""
                    cursor.execute(sql,(cedulaCliente,cedulaTendero))
                    resultado_id = cursor.fetchone()
                    id_Cliente = resultado_id["idCliente"]
                    sql = """INSERT INTO creditos (idVentas,idCliente) VALUES(%s,%s)"""
                    cursor.execute(sql,(idVenta,id_Cliente))
                    conexion.commit()
                    sql = """UPDATE cliente SET saldo = saldo + %s WHERE idCliente = %s AND idTendero = %s;"""
                    cursor.execute(sql,(valor,id_Cliente,cedulaTendero,))
                    conexion.commit()
                    return jsonify("resultado")
            else:
                 return jsonify("sinResultado")
        except Exception as e:
                    return jsonify("error")
        
    @app.route("/buscar_cliente", methods =['POST'])
    def buscar():
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        data = request.get_json()
        identificacion = data['cedula']
        tendero = data['idTendero']
        sql = "SELECT * FROM cliente where idTendero=%s and cedula=%s"
        cursor.execute(sql,(tendero, identificacion,))
        resultado = cursor.fetchone()
        print(resultado)
        if resultado:
            return jsonify(resultado)
        return jsonify({"nombre":None, "saldo":None})

    @app.route("/insertar_cliente", methods =['POST'])    
    def insertar_cliente():
        try:
            conexion = obtenerConexion()
            cursor = conexion.cursor(dictionary=True)
            data = request.get_json()
            print(f"los datos insert cliente son ",data)
            cedulaCliente = data['cedulaCliente']
            cedulaTendero = data['cedulaTendero']
            nombre = data['nombre']
            celular = data['celular']
            sql = "INSERT INTO cliente(cedula,idTendero,nombre,telefono) values (%s,%s,%s,%s) "
            cursor.execute(sql,(cedulaCliente,cedulaTendero,nombre,celular))
            conexion.commit()
            return jsonify(True)
        except Exception as e:
            return jsonify(False)
        

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
