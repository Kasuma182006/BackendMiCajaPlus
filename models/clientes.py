from conexion import obtenerConexion

class Clientes:


    def ConsultarClientes(self, cedula):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM clientes WHERE cedula = %s", (cedula.strip(),)
        )
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado
    
    def insertar_cliente(self, data_cliente):
        conexion = obtenerConexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO clientes (cedula, nombre, telefono, idTendero) VALUES (%s, %s, %s, %s)",
            (data_cliente['cedula'], data_cliente['nombre'], data_cliente['telefono'],data_cliente['tendero'])
        )
        conexion.commit()
        cursor.close()
        conexion.close()

