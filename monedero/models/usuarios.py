from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm
import bcrypt
class UsuarioModel (base_de_datos.Model):
    __tablename__='usuarios'

    usuarioId=Column(name='id', type_=types.Integer, primary_key=True,
                    unique=True, autoincrement=True, nullable=False)

    usuarioNombre=Column(name='nombre', type_=types.String(length=45))
    usuarioApellido=Column(name='apellido', type_=types.String(length=45))
    usuarioCorreo=Column(name='correo', type_=types.String(length=45), unique=True)
    usuarioPassword=Column(name='password', type_=types.Text)

    movimientos = orm.relationship('MovimientoModel', backref='usuarioMovimiento')


    def __init__(self, nombre, apellido, correo, password):
        self.usuarioNombre = nombre
        self.usuarioApellido = apellido
        self.usuarioCorreo = correo
        # ENCRIPTAR LA PASSWORD
        # primero agarro el password y lo convierto en bytes mediante el formato de escritura utf-8
        passwordBytes = bytes(password, "utf-8")
        # el metodo hashpw agarra la contraseña y un salt generado aleatoriamente para fusionarlos y luego devolver la contraseña hasheada (en forma de un hash)
        passwordHash = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
        # el metodo decode convierte el tipo de dato bytes a str
        passwordString = passwordHash.decode("utf-8")
        self.usuarioPassword = passwordString
        # self.usuarioPassword = password

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def json(self):
        return{
            "usuarioId": self.usuarioId,
            "usuarioNombre":self.usuarioNombre,
            "usuarioApellido":self.usuarioApellido,
            "usuarioCorreo":self.usuarioCorreo
        }
