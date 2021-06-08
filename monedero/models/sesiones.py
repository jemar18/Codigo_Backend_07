from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types

class SesionModel (base_de_datos.Model):
    __tablename__='sesiones'

    sesionId=Column(name='id', type_=types.Integer, primary_key=True,
                    unique=True, autoincrement=True, nullable=False)

    sesionToken=Column(name='token', type_=types.String(length=45))
    sesionEstado=Column(name='estado', type_=types.Boolean)
    sesionVencimiento=Column(name='vencimiento', type_=types.DateTime)


    def __init__(self, token, estado, vencimiento):
        self.sesionToken=token
        self.sesionEstado=estado
        self.sesionVencimiento=vencimiento