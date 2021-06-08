from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm

class UsuarioModel (base_de_datos.Model):
    __tablename__='usuarios'

    usuarioId=Column(name='id', type_=types.Integer, primary_key=True,
                    unique=True, autoincrement=True, nullable=False)

    usuarioNombre=Column(name='nombre', type_=types.String(length=45))
    usuarioApellido=Column(name='apellido', type_=types.String(length=45))
    usuarioCorreo=Column(name='correo', type_=types.String(length=45))
    usuarioPassword=Column(name='password', type_=types.Text)

    movimientos = orm.relationship('MovimientoModel', backref='usuarioMovimiento')


    def __init__(self, nombre, apellido, correo, password):
        self.usuarioNombre=nombre
        self.usuarioApellido=apellido
        self.usuarioCorreo=correo
        self.usuarioPassword=password