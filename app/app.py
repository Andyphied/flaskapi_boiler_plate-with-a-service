from flask import Blueprint
from flask_restplus import Api
from resources.errors import errors
from resources.auth import api as user_ns
from resources.auth import api_auth as auth_ns
from resources.carservice import api as car_service_ns


api_bp = Blueprint('api', __name__)

api = Api(api_bp,
        title='MOCK API FRAMEWORK WITH JWT',
        version='0.10',
        description='there is still more to come',
        errors=errors)


#Routes
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(car_service_ns, path='/cs')
