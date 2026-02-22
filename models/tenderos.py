from conexion import obtenerConexion

class Tenderos:
    
    def crear_tendero(self,cedula,hash_telefono,nombre):
        conexion = obtenerConexion()
        cursor = conexion.cursor()
        sql = "INSERT INTO tendero (cedula,llave,nombre) VALUES (%s, %s, %s)"
        cursor.execute(sql, (cedula,hash_telefono,nombre))
        conexion.commit()
        resultado=cursor.rowcount
        cursor.close()
        conexion.close()
        return resultado

    def validar_login(self, cedula):
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT * FROM tendero WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
        resultado=cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado