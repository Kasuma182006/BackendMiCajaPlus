from conexion import obtenerConexion

class Clientes:

    def ConsultarClientes(self, datos):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cliente WHERE cedula = %s AND idTendero=%s",
                       (datos['cedula'],datos['idTendero']))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado
    
    
    def actualizarSaldo(self,cedulaCliente,cedulaTendero,saldo):
        conexion=obtenerConexion()
        cursor=conexion.cursor()
        cursor.execute("UPDATE cliente SET saldo = %s WHERE cedula = %s AND idTendero = %s",
                       (saldo,cedulaCliente,cedulaTendero))
        conexion.commit()
        resultado=cursor.rowcount
        cursor.close()
        conexion.close()
        return resultado
    
    def insertar_cliente(self, data_cliente):
        conexion = obtenerConexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO cliente (idTendero,cedula, nombre, telefono,saldo) VALUES (%s,%s,%s,%s,%s)",
            (data_cliente['idTendero']),data_cliente['cedula'],data_cliente['nombre'],data_cliente['telefono'],
            data_cliente['saldo'])
        conexion.commit()
        cursor.close()
        conexion.close()

