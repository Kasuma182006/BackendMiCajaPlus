import mysql.connector


def obtenerConexion():
    return mysql.connector.connect(host="localhost",
                                   user="root",
                                   port = 3307,
                                   password = "",
                                   database="micajaplus")

###return mysql.connector.connect(host="localhost",
                                   ##user="micajadb_admin",
                                   ##password = "MyBox25Admin*",
                                   ##database="micajaplus")