from datetime import timedelta
from flask import Flask, app, request
from dotenv import load_dotenv

from config.conexion_bd import base_de_datos
from os import environ, path
from controllers.movimientos import MovimientosController
from models.sesiones import SesionModel
from controllers.usuario import RegistroController
from flask_restful import Api
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from config.custom_jwt import manejo_error_JWT

load_dotenv()
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='clavesecreta'

app.config['JWT_EXPIRATION_DELTA']=timedelta(hours=1)
app.config['JWT_AUTH_URL_RULE']='/login'
app.config['JWT_AUT_USERNAME_KEY']='correo'
app.config['MAX_CONTENT_LENGTH']=1*1024*1024

base_de_datos.init_app(app)
#base_de_datos.drop_all(app=app)
base_de_datos.create_all(app=app)

jsonwebtoken = JWT(app=app, authentication_handler=autenticador,
                   identity_handler=identificador)

jsonwebtoken.jwt_error_callback=manejo_error_JWT

api=Api(app)
api.add_resource(RegistroController, "/registro")
api.add_resource(MovimientosController, "/movimientos")

# @app.route("/")
# def initial_controller():
#     return{
#         "message":"Bienvenido a mi API de Monedero"
#     }

extensiones= {'pdf', 'png', 'jpg', 'jpeg'}
def archivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in extensiones

@app.route("/subirArchivo", methods=['POST'])
def subir_archivo():
  
   print(request.files)
   archivo=request.files['archivo']
   print(archivo.filename)
   print(archivo.mimetype)
   if archivos_permitidos(archivo.filename):
        archivo.save(path.join("multimedia",archivo.filename))
        return 'ok'
   else:
       return "Archivo no Permitido"

if __name__=="__main__":
    app.run(debug=True)