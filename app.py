from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from routes.clientes import cargar_rutas_clientes
# from routes.creditos import cargar_rutas_credito
from routes.tenderos import cargar_rutas_Tenderos
from routes.operaciones import cargar_rutas_operaciones
from routes.estadisticas import cargar_rutas_estadisticas
from routes.inventario import cargar_rutas_inventario
from routes.abonos import cargar_ruta_abonos
from routes.sesion import cargar_rutas_sesion

app=Flask(__name__)
app.secret_key = "micajaplus_secret_key"

app.permanent_session_lifetime = timedelta(hours=12)

CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:5500", "http://localhost:5500"]
)


cargar_rutas_operaciones(app)
cargar_rutas_clientes(app)
# cargar_rutas_credito(app)
cargar_rutas_Tenderos(app)
cargar_rutas_estadisticas(app)
cargar_rutas_inventario(app)
cargar_ruta_abonos(app)
cargar_rutas_sesion(app)

if __name__== '__main__':
    app.run(host='0.0.0.0', debug =True ,port=4000)