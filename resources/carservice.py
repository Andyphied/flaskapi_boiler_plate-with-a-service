import datetime

from flask import request
from database.models import CarServiceDataModel, CarServiceDataSchema, db
from utils.dto import CarServiceDto
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource
from resources.errors import InternalServerError,NoAuthorizationError

import random

api = CarServiceDto.api
_service = CarServiceDto.car_service

car_schema = CarServiceDataSchema()

@api.route('/car_service')
class CarService(Resource):    

    @jwt_required
    @api.response(201, 'Car Price Sucessfully Predicted')
    @api.doc('Make car price predictions')
    @api.expect(_service, validate=True)
    def post(self):
        try:
            data = request.get_json()
            data = car_schema.load(data)
            car_service_data = CarServiceDataModel(
                car_model= data['car_model'],
                date =datetime.datetime.now()
            )
            db.session.add(car_service_data)
            db.session.commit()
            #MODEL PREDICTION
            return {'price': int(random.randrange(500000, 50000000))}, 200
        except NoAuthorizationError:
            raise NoAuthorizationError
        except Exception as e:
            print(e)
            raise InternalServerError


