from flask import Flask, app
from dotenv import load_dotenv
from config.conexion_bd import base_de_datos
from os import environ
from models.usuarios import UsuarioModel
from models.movimientos import MovimientoModel

load_dotenv()
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

base_de_datos.init_app(app)
base_de_datos.drop_all(app=app)
base_de_datos.create_all(app=app)

@app.route("/")
def initial_controller():
    return{
        "message":"Bienvenido a mi API de Monedero"
    }


if __name__=="__main__":
    app.run(debug=True)