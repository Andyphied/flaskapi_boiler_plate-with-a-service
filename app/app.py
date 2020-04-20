from flask import Blueprint
from flask_restplus import Api
from resources.errors import errors


api_bp = Blueprint('api', __name__)

api = Api(api_bp, errors=errors)




#Routes

