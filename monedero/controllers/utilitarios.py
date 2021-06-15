from re import search, fullmatch
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

class Utilitarios(Resource):
    def validarCorreo(self,correo,patron_correo):        
            if search(patron_correo, correo):
                try:               
                    return True, 201
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

    # def validarPassword(self,password,patron_password):        
    #         if fullmatch(patron_password, password):
    #             try:               
    #                 return True, 201
    #             except IntegrityError as error:
    #                 print(error)
    #                 return {
    #                     "success": False,
    #                     "content": None,
    #                     "message": "Correo ya existe"
    #                 }, 400
    #             except:
    #                 return{
    #                     "success": False,
    #                     "content": None,
    #                     "message": "Error inesperado!"
    #                 }, 400
    #         else:
    #             return {
    #                 "success": False,
    #                 "content": None,
    #                 "message": "Correo incorrecto"
    #             }, 400