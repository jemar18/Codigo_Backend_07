from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, ForeignKey

class MovimientoModel (base_de_datos.Model):
    __tablename__='movimientos'

    movimientoId=Column(name='id', type_=types.Integer, primary_key=True,
                    unique=True, autoincrement=True, nullable=False)

    movimientoNombre=Column(name='nombre', type_=types.String(length=45))
    movimientoMonto=Column(name='monto', type_=types.Float)
    movimientoFecha=Column(name='fecha', type_=types.DateTime)
    movimientoImagen=Column(name='imagen', type_=types.Text)
    movimientoTipo=Column(name='tipo', type_=types.String(length=45))
    
    usuario=Column(ForeignKey(column='usuarios.id',ondelete='CASCADE'), 
                    name='usuarios_id', type_=types.Integer)

    def __init__(self, nombre, monto, fecha, imagen, tipo, usuario_id):
        self.movimientoNombre=nombre
        self.movimientoMonto=monto
        self.movimientoFecha=fecha
        self.movimientoImagen=imagen
        self.movimientoTipo=tipo
        self.usuario=usuario_id

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()
    
    def json(self):
        return {
            "movimientoId": self.movimientoId,
            "movimientoNombre": self.movimientoNombre,
            "movimientoMonto": self.movimientoMonto,
            "movimientoFecha": str(self.movimientoFecha),
            "movimientoImagen": self.movimientoImagen,
            "movimientoTipo": self.movimientoTipo,
        }