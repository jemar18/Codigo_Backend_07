from flask_restful import Resource, reqparse, request
from sqlalchemy.sql.expression import false
from models.usuarios import UsuarioModel
from sqlalchemy.exc import IntegrityError
from re import search, fullmatch
from cryptography.fernet import Fernet
from os import environ, link
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from config.conexion_bd import base_de_datos
from utils.enviar_correo_puro import enviarCorreo

load_dotenv()
PATRON_CORREO='^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
class RegistroController(Resource):

    
    
    serializer=reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'nombre',  
        type=str,
        required=True,     
        help="Falta el nombre",
        location='json'
    )
    serializer.add_argument(
        'apellido',  
        type=str,
        required=True,     
        help="Falta el apellido",
        location='json'
    )
    serializer.add_argument(
        'correo',  
        type=str,
        required=True,     
        help="Falta el correo",
        location='json'
    )
    serializer.add_argument(
        'password',  
        type=str,
        required=True,     
        help="Falta el password",
        location='json'
    )
    
    def post(self):
        data = self.serializer.parse_args()
        correo = data.get('correo')
        # ^ => tiene que coincidir el comienzo de la cadena
        # [a-zA-Z0-9] => significa que el texto tiene que coincidir con una letra minuscula y una letra mayuscula y un numero+
        # [\._] => coincidir con el punto o sub guion
        # ? => encontrar 0 o 1 coincidencia
        # + => la combinacion del texto anterior se puede repetir mas de una vez
        # [@] => que luego si o si tiene que haber un arroba
        # \w => coincida con cualquier caracter alfanumerico
        # [.] => luego si o si tiene que haber un .
        # {2,3} => indico que ese texto alfanumerico va a tener una longitud minima de 2 y una maxima de 3 caracteres
        # $ => indica que tiene que coincidir el final de la cadena
       
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        password = data.get('password')
        # VALIDAR MEDIANTE REGEXP si la contraseña tiene al menos 8 caracteres de longitud y al menos un numero, una letra min, una letra mayus
        # al menos una minus, mayus, un numero y un caracter especial @$!%*#&?
        # (m,n) => coincidencia entre esos patrones
        # * => match entre 0 y mas repeticiones
        # . => match con cualquier caracter excepto un salto de linea
        # [...] => match con cualquiera de los caracteres indicados dentro de los corchetes
        patron_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#&?])[A-Za-z\d@$!%*#&?]{6,}$'
        # fullmatch => require el string completo para que cumpla la expresion regular y no solamente una porcion
        if search(PATRON_CORREO, correo) and fullmatch(patron_password, password):
            try:
                nuevoUsuario = UsuarioModel(nombre, apellido, correo, password)
                nuevoUsuario.save()
                return {
                    "success": True,
                    "content": nuevoUsuario.json(),
                    "message": "Usuario registrado exitosamente"
                }, 201
            except IntegrityError as error:
                print(error)
                return {
                    "success": False,
                    "content": None,
                    "message": "Correo ya existe"
                }, 400
            except:
                return{
                    "success": False,
                    "content": None,
                    "message": "Error inesperado!"
                }, 400
        else:
            return {
                "success": False,
                "content": None,
                "message": "Correo incorrecto"
            }, 400

class ForgotPasswordController(Resource):
    serializer=reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'correo',  
        type=str,
        required=True,     
        help="Falta el correo",
        location='json'
    )

    def post(self):
        data=self.serializer.parse_args()
        correo=data['correo']
        fernet=Fernet(environ.get("FERNET_SECRET"))
        
        if search(PATRON_CORREO, correo):
            usuario= base_de_datos.session.query(UsuarioModel).filter_by(usuarioCorreo=correo).first()
            if not usuario:            
                return {
                    "success": False,
                    "content": None,
                    "message": "Usuario no encontrado"
                }, 404  

            payload={
                "fecha_caducidad":str(datetime.now()+timedelta(minutes=30)),
                "correo":correo
            }
            print(payload)
            payload_json=json.dumps(payload)
        
            token=fernet.encrypt(bytes(payload_json,"UTF-8"))
            print(token)
            link = request.host_url+'/recuperarPassword'+str(token)
            respuesta=enviarCorreo(usuario.usuarioCorreo,usuario.usuarioNombre,link)
            # token_desen=fernet.decrypt(bytes(token,"UTF-8"))
            # print(token_desen)
            # return {
            #     "success":True,
            #     "content":token,
            #     "message":"Usuario encontrado"
            # }   
            if respuesta:      
                return 'ok' 
            else:
               return {
                "success": False,
                "content": None,
                "message": "error al enviar el correo"
            }, 500             
        else:
            return {
                "success": False,
                "content": None,
                "message": "Correo incorrecto"
            }, 400

          
            
        