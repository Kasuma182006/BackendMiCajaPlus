from flask import Flask
from flask_cors import CORS
from routes.clientes import cargar_rutas_clientes
from routes.creditos import cargar_rutas_credito
from routes.tenderos import cargar_rutas_Tenderos
from routes.operaciones import cargar_rutas_operaciones
from routes.estadisticas import cargar_rutas_estadisticas
from routes.inventario import cargar_rutas_inventario
app=Flask(__name__)
CORS(app)


cargar_rutas_operaciones(app)
cargar_rutas_clientes(app)
cargar_rutas_credito(app)
cargar_rutas_Tenderos(app)
cargar_rutas_estadisticas(app)
cargar_rutas_inventario(app)

if __name__== '__main__':
    app.run(host='0.0.0.0', debug =True ,port=4000)