from flask import Response, request
from database.models import CarServiceDataModel, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from resources.errors import InternalServerError,NoAuthorizationError

import random

class CarService(Resource):    
    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            car_service_data_model = CarServiceDataModel(**body)
            #MODEL PREDICTION
            return {'price': int(random.randrange(500000, 50000000))}, 200
        except NoAuthorizationError:
            raise NoAuthorizationError
        except Exception as e:
            raise InternalServerError


