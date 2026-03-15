import mysql.connector


def obtenerConexion():
    return mysql.connector.connect(host="localhost",
                                   user="root",
                                   port = 3306,
                                   password = "",
                                   database="micajitaplus")

###return mysql.connector.connect(host="localhost",
                                   ##user="micajadb_admin",
                                   ##password = "MyBox25Admin*",
                                   ##database="micajaplus")