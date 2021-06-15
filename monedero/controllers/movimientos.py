from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import text
from models.movimientos import MovimientoModel
from datetime import datetime
from flask_jwt import jwt_required, current_identity


# CREATE
# READ
class MovimientosController(Resource):
    movimientoSerializer = reqparse.RequestParser(bundle_errors=True)

    movimientoSerializer.add_argument(
        'nombre',
        type=str,
        required=True,
        help='Falta el nombre',
        location='json',
    )
    movimientoSerializer.add_argument(
        'monto',
        type=float,
        required=True,
        help='Falta el monto',
        location='json',
    )
    movimientoSerializer.add_argument(
        'fecha',
        type=str,
        required=False,
        location='json',
    )
    movimientoSerializer.add_argument(
        'imagen',
        type=str,
        required=False,
        location='json',
    )
    movimientoSerializer.add_argument(
        'tipo',
        type=str,
        required=True,
        help='Falta el tipo',
        location='json',
        choices=['ingreso', 'egreso']
    )

    # con el decorador jwt_required estoy indicando que este metodo de esta clase tiene que recibir una token (es protegida)
    @jwt_required()
    def post(self):
        print("La identidad es ")
        print(current_identity)
        data = self.movimientoSerializer.parse_args()
        print(data)
        try:           
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')          
        except:
            return {
                "success":False,
                "message":"Formato de fecha incorrecto, el formato es YYYY-MM-DD HH:MM:SS",
                "content":None
            }

        objMovimiento=MovimientoModel(data['nombre'],data['monto'],fecha,data['imagen'],data['tipo'],current_identity.get('usuarioId'))
        objMovimiento.save()
        return {
                "success":True,
                "message":"Registrado correctamente",
                "content":objMovimiento.json()
            }

    def get(self):
        pass